html-to-qif
===========

Convert HSBC HTML and PDF bank statements to Quicken QIF or CSV files.

Usage
-----

```
usage: html-to-qif [-h] [--year YEAR] [--format {pdf,html}]
                   [--output-format {qif,csv}] [--verbose]
                   input output

Convert an HSBC UK statement to different file formats.

positional arguments:
  input                 input HTML statement
  output                output QIF file

optional arguments:
  -h, --help            show this help message and exit
  --year YEAR, -y YEAR  statement year
  --format {pdf,html}, -f {pdf,html}
                        statement format
  --output-format {qif,csv}
                        output format
  --verbose, -v         Show verbose output.
```

License
-------

evernote-bookmarks is available under the MIT license. See the [LICENSE](LICENSE) file for more info.
