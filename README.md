html-to-qif
===========

Convert HSBC HTML and PDF bank statements to Quicken QIF or CSV files.

Dependencies
------------

1. Install [Homebrew](https://brew.sh).

2. Install `pdf2json`.

   ```bash
   brew install pdf2json
   ```

3. Install `pip` if it's not already installed.

   ```bash
   sudo easy_install pip
   ```

4. Install the Python requirements.

   ```bash
   pip install -r requirements.txt
   ```

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
