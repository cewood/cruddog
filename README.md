# cruddog

A really simple tool for performing crud operations on datadog dashboards (timeboards, screenboards), and useful for managing your dashboards as code.


## Prerequisites

Check the requirements.txt file for the python dependencies. You can either install these as a `pip install -r requirements.txt` style command and use cruddog locally via a `python cruddog.py ...` call, or you can globally install cruddog using a `python setup.py install` command... use whatever floats your boat.


## Examples

There's an examples directory provided with a few very simply scripts and dummy (empty) dashboards to illustrate how you could use this repo/script to manipulate your dashboards. Some of those scripts are using [Jq](https://stedolan.github.io/jq/) to remove a few fields from the backups for comparison (id, created, and modified fields), so if you want to use those you'll need to install Jq.
