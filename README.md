# co2-monitor
IoT system for writing co2 sensor value to GoogleSpreadSheet with Raspberry Pi.

# Setup
## Install Dependencies Packages
```bash
# install with pip
$ pip3 install -r requirements.txt
```

## Create Service Account
### By Website
```bash
# create service account
https://cloud.google.com/iam/docs/creating-managing-service-accounts
# enable sheet api
https://cloud.google.com/apis/docs/enable-disable-apis
```

### By command line
```bash
# login google suite
$ gcloud auth login
# create GCP project
$ gcloud projects create [PROJECT_ID]
# create service account
$ gcloud iam service-accounts create [SA-NAME] --display-name [SA-DISPLAY-NAME]
# generate service account key
$ gcloud iam service-accounts keys create ./key.json --iam-account [SA-NAME]@[PROJECT-ID].iam.gserviceaccount.com
# enable sheets api
$ gcloud services enable sheets.googleapis.com
```

## Add Sheet Permission
Create a GoogleSpreadSheet and from "Share" add the edit permission of the service account created above.

# Run
## Write CO2 Sensor to Google Spread Sheet
```bash
$ python3 handler.py --help
usage: handler.py [-h] -s SPREAD_SHEET_ID [-k KEY_PATH] [-i INTERVAL]

CO2 Sensor Script

optional arguments:
  -h, --help            show this help message and exit
  -s SPREAD_SHEET_ID, --spread-sheet-id SPREAD_SHEET_ID
                        set spread sheet id
  -k KEY_PATH, --key-path KEY_PATH
                        set service account key path (default ./key.json)
  -i INTERVAL, --interval INTERVAL
                        set script interval seconds (default 600 seconds)

# run script
$ python3 handler.py -s SPREAD_SHEET_ID [-k KEY_PATH] [-i INTERVAL]
```
