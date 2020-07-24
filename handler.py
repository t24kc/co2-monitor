from datetime import datetime
from time import sleep
from lib.spread_sheet import SpreadSheet
from sensor.CO2MINI import CO2MINI

import argparse
import schedule

DEFAULT_COLUMNS = ["Time", "CO2(ppm)"]
DEFAULT_SERVICE_ACCOUNT_PATH = "./key.json"
DEFAULT_INTERVAL_SECONDS = 600


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
    parser = argparse.ArgumentParser(description="CO2 Sensor Script")
    parser.add_argument(
        "-s",
        "--spread-sheet-id",
        type=str,
        required=True,
        help="set spread sheet id",
    )
    parser.add_argument(
        "-k",
        "--key-path",
        type=str,
        default=DEFAULT_SERVICE_ACCOUNT_PATH,
        help="set service account key path (default {})".format(DEFAULT_SERVICE_ACCOUNT_PATH),
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=DEFAULT_INTERVAL_SECONDS,
        help="set script interval seconds (default {} seconds)".format(DEFAULT_INTERVAL_SECONDS),
    )
    args = parser.parse_args()

    scheduler = Scheduler(args)
    schedule.every(args.interval).seconds.do(
        scheduler.monitoring_job
    )

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    main()
