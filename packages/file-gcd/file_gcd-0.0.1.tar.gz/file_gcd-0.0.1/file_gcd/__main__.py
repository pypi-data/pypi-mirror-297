"""Get GCD of input file with filtering, provide python API."""
import argparse
import logging
import math
import sys
from typing import List, Dict, Any
from functools import reduce

import pandas as pd


def get_args() -> argparse.Namespace:
    """Get arguments from program call via sys.argv."""
    parser = argparse.ArgumentParser(description=f"{__file__.__doc__}")

    parser.add_argument("--input_file", "-i",
                        help=('File formatted as CSV with col headers '
                              'ID, PROPERTY, NUM1, NUM2, ... '),
                        metavar="path_to/input_data.csv")
    parser.add_argument("--output_file", "-o",
                        help=('File formatted as CSV with col headers '
                              'ID, PROPERTY, GCD. If not provided, '
                              'result is printed to stdout.'),
                        metavar="path_to/result.csv")
    parser.add_argument("--property_startswith", "-s",
                        help=('GCD will be calculated for rows only where '
                              'PROPERTY column must start with this string '
                              '(default: %(default)s)'),
                        default="000",
                        metavar="XYZ")

    logging.info("Arguments are parsed")
    return parser.parse_args(sys.argv[1:])


def gcd_list(vals: List[int]) -> int:
    """Get GCD for list of ints.

    Parameters
    ----------
    vals : List[int]
        GCD for all the values is calcualted.

    Returns
    -------
    int
        The GCD for the whole list, single value.
    """
    return reduce(math.gcd, vals)


def select_nums(row: Dict[str, Any]) -> List[int]:
    """Given an iterable row, return the values with keys starting with NUM."""
    ret = [val for key, val in row.items() if key.startswith("NUM")]
    return ret


def main():
    """C-styled main function."""
    args = get_args()
    nums = pd.read_csv(args.input_file, index_col="ID")
    nums = nums[nums["PROPERTY"].str.startswith(args.property_startswith)]
    res = nums.apply(lambda row: gcd_list(select_nums(row)), axis=1)
    merged = pd.concat([nums[["PROPERTY"]],
                        pd.DataFrame(res, columns=['GCD'])], axis=1)
    if args.output_file is None:
        print(merged)
    else:
        merged.to_csv(args.output_file)


if __name__ == "__main__":
    main()
