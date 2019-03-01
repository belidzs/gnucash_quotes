# Alpha Vantage to GnuCash quote downloader

This script can import daily stock and forex quotes from [Alpha Vantage](https://www.alphavantage.co/) and insert them 
into [GnuCash](https://gnucash.org/)'s database.

## Features
* Connect to any type of GnuCash data source supported by [piecash](https://github.com/sdementen/piecash) 
(*.gnucash files, relational databases, plain XML, etc)
* It can run even without GnuCash installed
* Automatic throttling to avoid over-polling
* Ignores price if it was already downloaded that day

## Requirements
* Python 3
* [piecash](https://github.com/sdementen/piecash)
* [alpha-vantage](https://github.com/RomelTorres/alpha_vantage)
* python-dateutil

## Install requirements
Just run `pip install -r requirements.txt`

It is recommended to install dependencies inside a dedicated virtualenv.

## Usage
Edit script to set up

* Alpha Vantage API key 
* Connection parameters
* Namespace - currency pairs

Run: `python gnucash_quotes.pty`
