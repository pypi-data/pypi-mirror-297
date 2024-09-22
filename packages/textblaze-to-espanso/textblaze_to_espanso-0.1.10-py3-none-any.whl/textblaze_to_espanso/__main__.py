import os.path

import loguru
from dotenv import load_dotenv

import argparse


def parse_arguments():
    loguru.logger.debug("Parsing arguments")
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--env-file", type=str, help="Path to env file for the package "
    )
    args = parser.parse_args()
    if args.env_file:
        if os.path.exists(args.env_file):
            loguru.logger.debug(f"Loading {args.env_file}")
            load_dotenv(args.env_file)
            print(f"Loaded environment variables from {args.env_file}")
        else:
            print(f"File {args.env_file} does not exist.")
            exit(1)


if __name__ == "__main__":
    parse_arguments()
    from textblaze_to_espanso.converter import TextBlazeToEspansoConverter

    TextBlazeToEspansoConverter().convert()
