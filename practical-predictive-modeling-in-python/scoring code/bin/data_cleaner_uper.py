#!/usr/bin/env python
# encoding: utf-8
"""
data_cleaner_uper.py
Created by Robert Dempsey on 2/24/15.
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

def format_claim_state(claim_state):
    """
    Helper function to properly format a claim state
    :param claim_state: an unformatted claim state straight from the database; eg 'release_verified'
    :return: claim state formatted like 'Release Verified'
    """
    claim_state = claim_state.replace("_"," ")
    claim_state = claim_state.title()
    return claim_state