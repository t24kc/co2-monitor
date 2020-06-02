from datetime import datetime
from time import sleep
from lib.spread_sheet import SpreadSheet
from sensor.CO2MINI import CO2MINI

import argparse
import schedule
import yaml

DEFAULT_COLUMNS = ["Time", "CO2(ppm)"]


class Scheduler:
    def __init__(self, args):
        self._co2mini_sensor = CO2MINI()
        self._spread_sheet_client = SpreadSheet(
            args.key_path, args.spread_sheet_id
        )
        if not self._spread_sheet_client.get_label_value("A1"):
            self._spread_sheet_client.append_row(DEFAULT_COLUMNS)

    def monitoring_job(self):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._co2mini_sensor.read_data()
        co2 = self._co2mini_sensor.get_co2()

        values = [
            current_datetime,
            round(co2, 1)
        ]
        print(values)
        self._spread_sheet_client.append_row(values)


def main():
    with open("config.yaml") as file:
        config = yaml.full_load(file)

    parser = argparse.ArgumentParser(description="Google Spread Sheet Script")
    parser.add_argument(
        "-k",
        "--key-path",
        type=str,
        default=config["google"]["service_account_path"],
        help="set service account key path (default {})".format(config["google"]["service_account_path"]),
    )
    parser.add_argument(
        "-s",
        "--spread-sheet-id",
        type=str,
        default=config["google"]["spread_sheet_id"],
        help="set spread sheet id",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=config["scheduler"]["monitoring_interval_minutes"],
        help="set script interval minutes (default {} minutes)".format(
            config["scheduler"]["monitoring_interval_minutes"]
        ),
    )
    args = parser.parse_args()

    scheduler = Scheduler(args)
    schedule.every(config["scheduler"]["monitoring_interval_minutes"]).minutes.do(
        scheduler.monitoring_job
    )

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
