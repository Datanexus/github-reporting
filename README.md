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
###Australia
Dump everything (this sometimes throws up on the proxy):

    PYTHONHTTPSVERIFY=0 ./eddiebot.py https://github.customerlabs.com.au/api/v3 67d65fba5616bf953466e30ba0e41eeb33c58ae7

or the proxy-safe version:

    for repo in iagcl/infrastructure-automation iagcl/app-automation iagcl/AWS-Devel iagcl/iag-svx iagcl/align iagcl/cl-analytics iagcl/git-workshops iagcl/iag-svx-deploy iagcl/tableau iagcl/informatica-extracts iagcl/mdm iagcl/edh-unit-test-vm iagcl/iag-edh-utilities iagcl/geo_analytics iagcl/geo_perils iagcl/geo_programme iagcl/geo_utilities iagcl/geo_web iagcl/iag-edh-sor iagcl/iag-edh-bus-ref iagcl/iag-edh-ctx-ctxtn iagcl/iag-edh-pub iagcl/iag-edh iagcl/location_engineering iagcl/geo_locate iagcl/rem_client iagcl/edh-greenplum-vm iagcl/cl-datamgmt-abn-bulk-data-extract iagcl/cl-datamgmt-edh-security; do
        PYTHONHTTPSVERIFY=0 /tmp/github-reporting/eddiebot.py --repo $repo https://github.customerlabs.com.au/api/v3 67d65fba5616bf953466e30ba0e41eeb33c58ae7
    done
