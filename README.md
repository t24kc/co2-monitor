# co2-monitor
IoT system for writing co2 sensor value to GoogleSpreadSheet with Raspberry Pi.

# Setup
## Install Dependencies Packages
```zsh
# install with pip
$ pip3 install -r requirements.txt

# install with poetry
$ poetry install
```

## Create Service Account
### By Website
```zsh
# create service account
https://cloud.google.com/iam/docs/creating-managing-service-accounts
# set gcp path
$ mv key.json .gcp/key.json
# enable sheet api
https://cloud.google.com/apis/docs/enable-disable-apis
```

### By command line
```zsh
# login google suite
$ gcloud auth login
# create GCP project
$ gcloud projects create [PROJECT_ID]
# create service account
$ gcloud iam service-accounts create [SA-NAME] --display-name [SA-DISPLAY-NAME]
# generate service account key
$ gcloud iam service-accounts keys create .gcp/key.json --iam-account [SA-NAME]@[PROJECT-ID].iam.gserviceaccount.com
# enable sheets api
$ gcloud services enable sheets.googleapis.com
```

## Add Sheet Permission
Create a GoogleSpreadSheet and from "Share" add the edit permission of the service account created above.

# Run
## Write CO2 Sensor to Google Spread Sheet
```zsh
$ python3 handler.py --help
usage: handler.py [-h] [-k KEY_PATH] [-s SPREAD_SHEET_ID] [-i INTERVAL]

Google Spread Sheet Script

optional arguments:
  -h, --help            show this help message and exit
  -k KEY_PATH, --key-path KEY_PATH
                        set service account key path (default .gcp/key.json)
  -s SPREAD_SHEET_ID, --spread-sheet-id SPREAD_SHEET_ID
                        set spread sheet id
  -i INTERVAL, --interval INTERVAL
                        set script interval minutes (default 10 minutes)

# update spread_sheet_id field in config file
$ edit config.yaml

# run script
$ python3 handler.py
```
