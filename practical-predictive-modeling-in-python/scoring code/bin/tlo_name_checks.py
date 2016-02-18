#!/usr/bin/env python
# encoding: utf-8
"""
tlo_name_checks.py
Created by Robert Dempsey on 05/18/2015
Updated on 05/18/2015
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

from fuzzywuzzy import fuzz


def exact_name_check(name_to_test, parts):
  """
  Test if a name comprises all or a subset of parts
  Returns True if name comprises any subset of parts
  """

  if parts is None:
    return 0

  if type(name_to_test) is not str:
   return 0


  for p in sorted(parts, key=len, reverse=True):
      name_to_test = name_to_test.replace(p, '', 1)
      if name_to_test == '':
          return 1
  return 0


def last_name_check(tlo_last_name_1, tlo_last_name_2, last_name_to_check):
  if last_name_to_check_inner(tlo_last_name_1, last_name_to_check) == 1:
      return 1

  if last_name_to_check_inner(tlo_last_name_2, last_name_to_check) == 1:
      return 1

  return 0


def last_name_to_check_inner(tlo_last_name, last_name_to_check):
    if tlo_last_name == last_name_to_check:
        return 1

    if last_name_to_check in tlo_last_name:
        return 1

    if tlo_last_name in last_name_to_check:
        return 1

    return 0


def fuzzy_ratio(thing_1, thing_2):
  """
  Runs a simple fuzzy ratio check
  """
  return fuzz.ratio(thing_1, thing_2)



def fuzzy_token_sort_ratio(thing_1, thing_2):
  """
  Runs a simple fuzzy ratio check
  """
  return fuzz.token_sort_ratio(thing_1, thing_2)


def fuzzy_partial_ratio(thing_1, thing_2):
  """
  Runs a simple fuzzy ratio check
  """
  return fuzz.partial_ratio(thing_1, thing_2)




def fuzzy_ratio_check(full_name_check_value, name_one, name_two):
    """
    Runs a fuzzy ratio check if the record hasn't passed either a full name or name with initial check
    """
    if full_name_check_value == 0:
        return fuzz.ratio(name_one, name_two)
    
    return 0


def fuzzy_token_sort_ratio_check(full_name_check_value, name_one, name_two):
    """
    Runs a fuzzy token sort ratio check if the record hasn't passed either a full name or name with initial check
    """
    if full_name_check_value == 0:
        return fuzz.token_sort_ratio(name_one, name_two)
    
    return 0


def fuzzy_partial_ratio_check(full_name_check_value, name_one, name_two):
    """
    Runs a fuzzy partial ratio check if the record hasn't passed either a full name or name with initial check
    """
    if full_name_check_value == 0:
        return fuzz.partial_ratio(name_one, name_two)
    
    return 0