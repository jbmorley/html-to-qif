#!/usr/bin/env python

import argparse
import codecs
import datetime
import json
import logging
import os.path
import subprocess
import tempfile

import inseven.finance


PDF_TABLE_COLUMNS = ["Date", "Payment ", "type ", "and ", "details", "Paid ", "out", "Paid ", "in", "Balance"]
PDF_TABLE_START = ["BALANCE ", "BROUGHT ", "FORWARD"]
PDF_TABLE_END = ["BALANCE ", "CARRIED ", "FORWARD"]
PDF_POSITION_THRESHOLD = 20


def pdf2json(path):
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        subprocess.check_output(["/usr/local/bin/pdf2json", path, temp.name])
        with codecs.open(temp.name, "r", "ISO-8859-1") as f:
            return json.loads(f.read())


def line_matches_offset(line, strings, offset):
    try:
        for i, data in enumerate(strings):
            if line[i + offset]["data"] != data:
                return False
    except IndexError:
        return False
    return True


def line_matches(line, strings):
    if len(line) < len(strings):
        return False
    else:
        for i in xrange(0, len(line) - len(strings) + 1):
            if line_matches_offset(line, strings, i):
                return True
    return False


def lines_between(lines, start, end):
    result = []
    active = False
    for line in lines:
        if line_matches(line, start):
            active = True
            result.append(line)
        elif line_matches(line, end):
            active = False
        else:
            if active:
                result.append(line)
    return result


def format_number(text):
    return float(text.replace(",", ""))


def parse_page(page, date=None):
    nodes = sorted(page["text"], key=lambda x: x["top"])

    # Group the individual nodes into lines.
    lines = []
    top = 0
    line = []
    for node in nodes:
        if node["top"] != top:
            line = []
            lines.append(line)
            top = node["top"]
        line.append(node)

    # Determine the column offsets.
    details = None
    for line in lines:
        if line_matches(line, PDF_TABLE_COLUMNS):
                details = [line[0]["left"], line[1]["left"], line[5]["left"], line[7]["left"], line[9]["left"]]

    # Filter out the lines we're interested in.
    statements = lines_between(lines, PDF_TABLE_START, PDF_TABLE_END)

    record = None
    results = []
    for line in statements:

        # Check to see if the row has changed.
        line = sorted(line, key=lambda x: x["left"])
        if line[0]["left"] == details[0] or line[0]["left"] == details[1] or record is None:
            record = inseven.finance.Record()
            results.append(record)

        # Process nodes for the current row.
        for node in line:
            logging.debug(line)
            left = node["left"]
            data = node["data"]
            if left >= details[4] - PDF_POSITION_THRESHOLD:
                logging.debug("Parsing '%s'..." % data)
                if data == "D":
                    record.balance = -1 * record.balance
                else:
                    record.balance = format_number(data)
            elif left >= details[3] - PDF_POSITION_THRESHOLD:
                # Paid in.
                record.value = format_number(data)
            elif left >= details[2] - PDF_POSITION_THRESHOLD:
                # Paid out.
                record.value = (format_number(data) * -1)
            elif left >= details[1]:
                record.description = (record.description + " " + data).strip()
            elif left > details[0]:
                date = (date + " " + data).strip()
            elif left == details[0]:
                date = data.strip()

            # Keep attempting to parse the date until we have a valid date.
            try:
                record.date = datetime.datetime.strptime(date, "%d %b %y")
            except ValueError:
                pass

    if not len(results):
        return (results, date, None)

    # Check and retrieve the starting balance.
    balance = results.pop(0)
    assert balance.description == "BALANCE BROUGHT FORWARD", "Unable to determine starting balance."

    return (results, date, balance.balance)


def parse_pdf(path):

    contents = pdf2json(path)

    results = []
    date = None
    starting_balance = None
    for page in contents:
        (records, date, balance) = parse_page(page, date)
        if starting_balance is None:
            starting_balance = balance
        results.extend(records)

    total = starting_balance
    for result in results:
        logging.debug("%s", result)
        total = total + result.value
        if result.balance is not None:
            assert abs(total - result.balance) < 0.0001, "Unable to reconcile balances"

    return results
