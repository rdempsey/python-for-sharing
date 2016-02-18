#!/usr/bin/env python
# encoding: utf-8
"""
cleaners.py
Created by Robert Dempsey on 05/18/2015
Updated on 05/18/2015
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import string
import csv

# Globals we need to work with
exclude = set(string.punctuation)

# suffixes will be a dict of all the suffixes that may be part of a last name
suffixes = {}
for i, line in enumerate(csv.reader(open("./utils/suffixes.csv"))):
    if i == 0:
        headers = line
        continue
    if line[1]:
        suffixes[line[0]] = line[1]


def remove_punctuation(x):
    """
    Helper function to remove punctuation from a string
    x: any string
    """
    try:
        x = ''.join(ch for ch in x if ch not in exclude)
    except:
        pass
    return x


def remove_suffixes(x):
    """
    Helper function to remove suffixes from a string
    x: any string
    """
    try:
        for suffix, description in suffixes.items():
            if x.endswith(" " + suffix):
                x = x[:-len(suffix)]
    except:
        pass
    return x


def remove_whitespace(x):
    """
    Helper function to remove any blank space from a string
    x: any string
    """
    try:
        x = "".join(x.split())
    except:
        pass
    return x


def remove_internal_abbreviations(x):
    """
    Helper function to remove things such as 'F/K/A' from a string
    x: any string
    """
    try:
        x = x.replace('F/K/A', "").replace("(MAIDEN", "").replace("(FKA", "").replace("(PREVIOUSLY", "").replace("(MAIDEN NAME", "").replace("(DECEASED) C/O", "")
    except:
        pass
    return x
