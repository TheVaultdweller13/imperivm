#!/bin/env python

import argparse
import parser as parser
import executor as executor


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename", nargs=1)
    args = argparser.parse_args()
    data = None
    with open(args.filename[0], "r") as file:
        code = file.read()

    ast = parser.ImperivmParser().parse(code)
    executor.ImperivmExecutor(ast).run()
