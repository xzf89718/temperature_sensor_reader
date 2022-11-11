# ref: https://github.com/HaralDev/GraphtecPython
from graphtec_reader.helper_function import readFromGraphtec
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Graphtec reader in python. Author: Zifeng XU, email: zifeng.xu@cern.ch.")
    parser.add_argument(
        "-p", "--port", help="Port for Graphtec.", required=True)
    parser.add_argument("-t", "--time-interval",
                        help="Baudrate for monitoring serial.", required=True)
    parser.add_argument("-o", "--outfile-name",
                        help="Timeout for monitoring serial.", required=True)
    args = parser.parse_args()
    print("All parameters get from commandline are:")
    print(args)

    PORT = args.port
    TIMEINTERVAL = args.time_interval
    OUTFILENAME = args.outfile_name

    readFromGraphtec(port=PORT, time_interval=TIMEINTERVAL,
                     logfile_name=OUTFILENAME)
