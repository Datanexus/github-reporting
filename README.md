# github-reporting
github repo and developer metrics

## Configure:
Run `pip install PyGitHub` on your Python 2.7.12+ installation.

## Run:
The code takes an API endpoint and API token as mandatory arguments. Unless you want to import certs, recommend you turn of cert validation during the run, as in:

    PYTHONHTTPSVERIFY=0 ./eddiebot.py ENDPOINT TOKEN

For CSV output, use the `--manager` flag:

    PYTHONHTTPSVERIFY=0 ./eddiebot.py --manager ENDPOINT TOKEN

To list all repos:

    PYTHONHTTPSVERIFY=0 ./eddiebot.py --list-repos REPO ENDPOINT TOKEN

To limit to a specific repo:

    PYTHONHTTPSVERIFY=0 ./eddiebot.py --repo REPO ENDPOINT TOKEN


## Reference:
[PyGitHub](http://pygithub.readthedocs.io/en/latest/reference.html)

## TL;DR
### Australia
Dump everything. Unset all proxy environment variables before running; the proxy dislikes rapid programatic API calls:

    PYTHONHTTPSVERIFY=0 ./eddiebot.py https://github.customerlabs.com.au/api/v3 67d65fba5616bf953466e30ba0e41eeb33c58ae7
