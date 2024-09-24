import argparse
import datetime
import os.path

import pandas as pd
import numpy as np

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(
    prog="oemof-tabular-plugins",
    description="Execute a scenario with oemof-tabular plugins",
    epilog="For more information see ...",
)
parser.add_argument(
    "-i",
    dest="dp_path",
    nargs="+",
    type=str,
    help="Path to the datapackage. Must be provided",
)
parser.add_argument(
    "-o",
    dest="results_path",
    nargs="+",
    type=str,
    help=f"Path to the output folder to save simulation results. If not provided, default output will be provided in {os.path.join(BASE_PATH, 'otp_results')}",
)


parser.add_argument(
    "--start-date",
    dest="date_start",
    type=datetime.date.fromisoformat,
    help="Date of start in YYYY-MM-DD format",
)

parser.add_argument(
    "-p",
    dest="parallel",
    default=False,
    const=True,
    nargs="?",
    type=bool,
    help="Whether or not the simulation uses parallel processing",
)

parser.add_argument(
    "-p",
    dest="parallel",
    default=False,
    const=True,
    nargs="?",
    type=bool,
    help="Whether or not the simulation uses parallel processing",
)


def main():
    args = vars(parser.parse_args())
    fnames = args["fname_path"]
    ofnames = args["ofname_path"]
    num_days = args["num_days"]
    # Define which input files should be considered and run.
    date_start = args["date_start"]
    date_end = args["date_end"]
    ext = args["extension"]
    parallel_processing = args["parallel"]

    years = args["years"]


if __name__ == "__main__":
    main()
