# -*- coding: utf-8 -*-

"""
rackcli.py

Apache License 2.0

Stuff
"""
import argparse
import config


def cli():
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='rackcli')
    parser.add_argument('-c', '--cfg', required=False, default=False,
                        help='optional configuration file path to use.')
    return parser.parse_args()
    # subparsers = parser.add_subparsers(help='sub-command help')


def main():
    args = cli()
    cfg = config.load_config(args.cfg)
    print cfg
