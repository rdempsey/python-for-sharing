#!/usr/bin/env python
# encoding: utf-8
"""
normalizers.py
Created by Robert Dempsey on 05/18/2015
Updated on 05/18/2015
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from time import strftime
from datetime import datetime
import bin.cleaners as clean


def right(s, amount):
    return s[-amount:]


def normalize_name(name):
    """
    Standardizes the name of a person by making it all caps

    name: full name of a person. can be in any format (John Smith,
            John M Smith, Smith, John, etc.)
    """
    try:
        name = name.upper()
    except:
        pass
    return name


def normalize_ssn(ssn):
    """
    Standardizes the SSN by removing any spaces, "XXXX", and dashes
    :param ssn: ssn to standardize
    :return: formatted_ssn
    """
    try:
        ssn = ssn.replace("-","")
        ssn = clean.remove_whitespace(ssn)
        if len(ssn) < 9 and ssn != 'Missing':
            ssn = "000000000" + ssn
            ssn = right(ssn, 9)
        
    except:
        pass

    return ssn


def normalize_dob(dob):
    """
    Standardizes the DOB
    :param dob: the dob to standardize
    :return formatted_dob
    """

    # Convert what we have to a string, just in case
    dob = str(dob)
    
    # Handle missing dates, however pandas should have filled this in as missing
    if not dob or dob.lower() == "missing" or dob == "nan":
        formatted_dob = "MISSING"

    # Handle dates from TLO that end with 'XXXX', start with 'XX', or are less than 1900
    if dob.lower().find('x') != -1:
        formatted_dob = "Incomplete"

    # Handle dates that start with something like "0056"
    if dob[0:2] == "00":
        dob = dob.replace("00", "19")

    # 03/03/15
    try:
        formatted_dob = str(datetime.strptime(dob, '%m/%d/%y').strftime('%m/%d/%y'))
    except:
        pass
    
    # 03/03/2015
    try:
        formatted_dob = str(datetime.strptime(dob, '%m/%d/%Y').strftime('%m/%d/%y'))
    except:
        pass

    # 0000-03-03
    try:
        if int(dob[0:4]) < 1900:
            formatted_dob = "Incomplete"
        else:
            formatted_dob = str(datetime.strptime(dob, '%Y-%m-%d').strftime('%m/%d/%y'))
    except:
        pass

    return formatted_dob
