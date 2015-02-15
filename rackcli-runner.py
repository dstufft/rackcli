#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Convenience wrapper for running rackcli directly from source tree instead of
 invoking odd and arcane setuptools wizardry."""


from rackcli.rackcli import cli


if __name__ == '__main__':
    cli()
