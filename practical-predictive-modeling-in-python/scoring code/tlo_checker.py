#!/usr/bin/env python
# encoding: utf-8
"""
tlo_checker.py
Created by Robert Dempsey on 03/02/2015
Updated by Robert Dempsey on 04/28/2015
Copyright (c) 2015 Robert Dempsey. All rights reserved.
"""

import pandas as pd
import numpy as np
import pickle
import string
import csv
from time import strftime
from datetime import datetime
import configparser
import os
import shutil
import bin.cleaners as clean
import bin.normalizers as norm
import bin.tlo_name_checks as nc
import bin.tlo_verification_and_matching as vm
import sys

# Globals we need to work with
exclude = set(string.punctuation)

# suffixes will be a dict of all the suffixes that may be part of a last name
suffixes = {}
for i, line in enumerate(csv.reader(open("./utils/suffixes.csv"))):
    if i==0:
        headers = line
        continue
    if line[1]:
        suffixes[line[0]] = line[1]

##
# HELPER FUNCTIONS
##

def get_tlo_send_date():
    """
    Create the date that the record was sent to tlo on
    Default: today
    """
    'YYYY-MM-DD HH:MM:SS'
    return strftime("%Y-%m-%d %H:%M:%S")

##
# Report Generation
##

def process_tlo_file(file_to_process, type_of_file):


    ##
    # Run the awesome
    ##

    print("{} - Preparing to run the TLO analysis".format(datetime.now()))

    # Read the config file and get the goodies
    config = configparser.ConfigParser()
    config.read('config/config.ini')
    base_path = config['TLO']['tlo_file_path']


    ##
    # Get the file information
    ##

    file_to_analyze = file_to_process
    report_type = type_of_file


    # Set up the paths, directories and file names we'll use
    report_file_name = "tlo_check_{}_{}_check_scores.csv".format(strftime("%m_%d_%y"), report_type)
    report_path = base_path + "TLO Checks {}".format(strftime("%m.%d.%y"))
    report_file = report_path +  "/" + report_file_name


    # Make the new directory
    if not os.path.exists(report_path):
      os.mkdir(report_path)


    print("{} - Retrieving the report data".format(datetime.now()))

    # Read the data
    df = pd.read_csv(file_to_analyze)


    ##
    # Preprocessing
    ##

    print("{} - Cleaning up the data".format(datetime.now()))

    # keep these for reference
    # Fields: sent_to_tlo_on,type,unique_claimant_id,last_name,first_name,date_of_birth,ssn,tlo_first_name_1,tlo_middle_name_1,tlo_last_name_1,tlo_first_name_2,tlo_middle_name_2,tlo_last_name_2,tlo_ssn,tlo_dob
    df['co_type'] = df.Type
    df['claim_number'] = df.claim_number
    df['last_name'] = df.last_name
    df['first_name'] = df.first_name
    df['date_of_birth'] = df.date_of_birth
    df['ssn'] = df.ssn
    df['tlo_first_name_1'] = df.TloName1FirstName
    df['tlo_middle_name_1'] = df.TloName1MiddleName
    df['tlo_last_name_1'] = df.TloName1LastName
    df['tlo_first_name_2'] = df.TloName2FirstName
    df['tlo_middle_name_2'] = df.TloName2MiddleName
    df['tlo_last_name_2'] = df.TloName2LastName
    df['tlo_ssn'] = df.TloSSN
    df['tlo_dob'] = df.TloDateOfBirth

    # Fill in missing data, use "inplace=TRUE" to ensure the data frame contents are changed
    df.tlo_first_name_1.fillna('Missing', inplace=True)
    df.tlo_middle_name_1.fillna('Missing', inplace=True)
    df.tlo_last_name_1.fillna('Missing', inplace=True)
    df.tlo_first_name_2.fillna('Missing', inplace=True)
    df.tlo_middle_name_2.fillna('Missing', inplace=True)
    df.tlo_last_name_2.fillna('Missing', inplace=True)
    df.tlo_ssn.fillna('Missing', inplace=True)
    df.tlo_dob.fillna('Missing', inplace=True)

    ##
    # Clean it all up
    ###

    # Remove internal abbreviations
    df.last_name = df.last_name.apply(clean.remove_internal_abbreviations)

    # Remove the punctuation
    df.first_name = df.first_name.apply(clean.remove_punctuation)
    df.last_name = df.last_name.apply(clean.remove_punctuation)
    df.tlo_first_name_1 = df.tlo_first_name_1.apply(clean.remove_punctuation)
    df.tlo_last_name_1 = df.tlo_last_name_1.apply(clean.remove_punctuation)
    df.tlo_first_name_2 = df.tlo_first_name_2.apply(clean.remove_punctuation)
    df.tlo_last_name_2 = df.tlo_last_name_2.apply(clean.remove_punctuation)

    # Remove suffixes from last names
    df.last_name = df.last_name.apply(clean.remove_suffixes)
    df.tlo_last_name_1 = df.tlo_last_name_1.apply(clean.remove_suffixes)
    df.tlo_last_name_2 = df.tlo_last_name_2.apply(clean.remove_suffixes)

    # Remove whitespace
    df.first_name = df.first_name.apply(clean.remove_whitespace)
    df.last_name = df.last_name.apply(clean.remove_whitespace)
    df.tlo_first_name_1 = df.tlo_first_name_1.apply(clean.remove_whitespace)
    df.tlo_last_name_1 = df.tlo_last_name_1.apply(clean.remove_whitespace)
    df.tlo_first_name_2 = df.tlo_first_name_2.apply(clean.remove_whitespace)
    df.tlo_last_name_2 = df.tlo_last_name_2.apply(clean.remove_whitespace)

    # Normalize the names
    df.first_name = df.first_name.apply(norm.normalize_name)
    df.last_name = df.last_name.apply(norm.normalize_name)

    # Normalize the SSN
    df.ssn = df.ssn.apply(norm.normalize_ssn)
    df.tlo_ssn = df.tlo_ssn.apply(norm.normalize_ssn)

    # Normalize the DOB
    df.date_of_birth = df.date_of_birth.apply(norm.normalize_dob)
    df.tlo_dob = df.tlo_dob.apply(norm.normalize_dob)


    # Create full names for comparison
    df['full_name'] = df.first_name + df.last_name

    df['tlo_name_combo_1'] = df.tlo_first_name_1 + df.tlo_middle_name_1
    df['tlo_name_combo_2'] = df.tlo_first_name_1 + df.tlo_last_name_1
    df['tlo_name_combo_3'] = df.tlo_first_name_1 + df.tlo_middle_name_2
    df['tlo_name_combo_4'] = df.tlo_first_name_1 + df.tlo_last_name_2
    df['tlo_name_combo_5'] = df.tlo_first_name_2 + df.tlo_middle_name_1
    df['tlo_name_combo_6'] = df.tlo_first_name_2 + df.tlo_last_name_1
    df['tlo_name_combo_7'] = df.tlo_first_name_2 + df.tlo_middle_name_2
    df['tlo_name_combo_8'] = df.tlo_first_name_2 + df.tlo_last_name_2
    df['tlo_name_combo_9'] = df.tlo_first_name_1 + df.tlo_middle_name_1 + df.tlo_last_name_1
    df['tlo_name_combo_10'] = df.tlo_first_name_2 + df.tlo_middle_name_2 + df.tlo_last_name_2
    df['tlo_name_combo_11'] = df.tlo_first_name_1 + df.tlo_last_name_1 + df.tlo_last_name_2
    df['tlo_name_combo_12'] = df.tlo_first_name_1 + df.tlo_last_name_2 + df.tlo_last_name_1
    df['tlo_name_combo_13'] = df.tlo_first_name_2 + df.tlo_last_name_1 + df.tlo_last_name_2
    df['tlo_name_combo_14'] = df.tlo_first_name_2 + df.tlo_last_name_2 + df.tlo_last_name_1

    ##
    # Run name check by removal
    ##

    print("{} - Running name checks".format(datetime.now()))

    # Name check ala Bob Flanders
    df['full_name_check_value'] = df.apply(lambda x: nc.exact_name_check(x['full_name'], [
                                                                                        x['tlo_first_name_1'], 
                                                                                        x['tlo_middle_name_1'], 
                                                                                        x['tlo_last_name_1'], 
                                                                                        x['tlo_first_name_2'], 
                                                                                        x['tlo_middle_name_2'], 
                                                                                        x['tlo_last_name_2']
                                                                                    ]), axis=1)

    # Last name check
    df['last_name_check_value'] = df.apply(lambda x: nc.last_name_check(x['tlo_last_name_1'], x['tlo_last_name_2'], x['last_name']), axis=1)


    ##
    # Features
    ##

    print("{} - Creating required features".format(datetime.now()))

    # SSN features
    df['ssn_ratio'] = df.apply(lambda x: nc.fuzzy_ratio(x['ssn'], x['tlo_ssn']), axis=1)
    df['ssn_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio(x['ssn'], x['tlo_ssn']), axis=1)
    df['ssn_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio(x['ssn'], x['tlo_ssn']), axis=1)

    # DOB features
    df['dob_ratio'] = df.apply(lambda x: nc.fuzzy_ratio(x['date_of_birth'], x['tlo_dob']), axis=1)
    df['dob_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio(x['date_of_birth'], x['tlo_dob']), axis=1)
    df['dob_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio(x['date_of_birth'], x['tlo_dob']), axis=1)

    # Name 1 features
    df['name_1_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_1']), axis=1)
    df['name_1_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_1']), axis=1)
    df['name_1_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_1']), axis=1)

    # Name 2 features
    df['name_2_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_2']), axis=1)
    df['name_2_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_2']), axis=1)
    df['name_2_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_2']), axis=1)

    # Name 3 features
    df['name_3_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_3']), axis=1)
    df['name_3_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_3']), axis=1)
    df['name_3_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_3']), axis=1)

    # Name 4 features
    df['name_4_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_4']), axis=1)
    df['name_4_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_4']), axis=1)
    df['name_4_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_4']), axis=1)

    # Name 5 features
    df['name_5_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_5']), axis=1)
    df['name_5_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_5']), axis=1)
    df['name_5_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_5']), axis=1)

    # Name 6 features
    df['name_6_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_6']), axis=1)
    df['name_6_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_6']), axis=1)
    df['name_6_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_6']), axis=1)

    # Name 7 features
    df['name_7_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_7']), axis=1)
    df['name_7_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_7']), axis=1)
    df['name_7_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_7']), axis=1)

    # Name 8 features
    df['name_8_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_8']), axis=1)
    df['name_8_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_8']), axis=1)
    df['name_8_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_8']), axis=1)

    # Name 9 features
    df['name_9_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_9']), axis=1)
    df['name_9_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_9']), axis=1)
    df['name_9_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_9']), axis=1)

    # Name 10 features
    df['name_10_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_10']), axis=1)
    df['name_10_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_10']), axis=1)
    df['name_10_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_10']), axis=1)

    # Name 11 features
    df['name_11_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_11']), axis=1)
    df['name_11_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_11']), axis=1)
    df['name_11_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_11']), axis=1)

    # Name 12 features
    df['name_12_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_12']), axis=1)
    df['name_12_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_12']), axis=1)
    df['name_12_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_12']), axis=1)

    # Name 13 features
    df['name_13_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_13']), axis=1)
    df['name_13_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_13']), axis=1)
    df['name_13_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_13']), axis=1)

    # Name 14 features
    df['name_14_ratio'] = df.apply(lambda x: nc.fuzzy_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_14']), axis=1)
    df['name_14_token_sort_ratio'] = df.apply(lambda x: nc.fuzzy_token_sort_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_14']), axis=1)
    df['name_14_partial_ratio'] = df.apply(lambda x: nc.fuzzy_partial_ratio_check(x['full_name_check_value'], x['full_name'], x['tlo_name_combo_14']), axis=1)


    ##
    # Scoring
    ##

    print("{} - Creating the scores".format(datetime.now()))

    df['ssn_score'] = df['ssn_ratio'] + df['ssn_token_sort_ratio'] + df['ssn_partial_ratio']
    df['dob_score'] = df['dob_ratio'] + df['dob_token_sort_ratio'] + df['dob_partial_ratio']

    df['n1_score'] = df['name_1_ratio'] + df['name_1_token_sort_ratio'] + df['name_1_partial_ratio']
    df['n2_score'] = df['name_2_ratio'] + df['name_2_token_sort_ratio'] + df['name_2_partial_ratio']
    df['n3_score'] = df['name_3_ratio'] + df['name_3_token_sort_ratio'] + df['name_3_partial_ratio']
    df['n4_score'] = df['name_4_ratio'] + df['name_4_token_sort_ratio'] + df['name_4_partial_ratio']
    df['n5_score'] = df['name_5_ratio'] + df['name_5_token_sort_ratio'] + df['name_5_partial_ratio']
    df['n6_score'] = df['name_6_ratio'] + df['name_6_token_sort_ratio'] + df['name_6_partial_ratio']
    df['n7_score'] = df['name_7_ratio'] + df['name_7_token_sort_ratio'] + df['name_7_partial_ratio']
    df['n8_score'] = df['name_8_ratio'] + df['name_8_token_sort_ratio'] + df['name_8_partial_ratio']
    df['n9_score'] = df['name_9_ratio'] + df['name_9_token_sort_ratio'] + df['name_9_partial_ratio']
    df['n10_score'] = df['name_10_ratio'] + df['name_10_token_sort_ratio'] + df['name_10_partial_ratio']
    df['n11_score'] = df['name_11_ratio'] + df['name_11_token_sort_ratio'] + df['name_11_partial_ratio']
    df['n12_score'] = df['name_12_ratio'] + df['name_12_token_sort_ratio'] + df['name_12_partial_ratio']
    df['n13_score'] = df['name_13_ratio'] + df['name_13_token_sort_ratio'] + df['name_13_partial_ratio']
    df['n14_score'] = df['name_14_ratio'] + df['name_14_token_sort_ratio'] + df['name_14_partial_ratio']

    ##
    # Final Verification
    ##

    print("{} - Analyzing the data".format(datetime.now()))

    # Determine if there is an SSN match
    df['ssn_match'] = df.apply(lambda x: vm.ssn_match(x['ssn_score']), axis=1)

    # Determine if there is a DOB match
    df['dob_match'] = df.apply(lambda x: vm.dob_match(x['dob_score']), axis=1)

    # Determine if there is a name match
    df['name_match'] = df.apply(lambda x: vm.name_match(x['full_name_check_value'], 
                                                     x['last_name_check_value'],
                                                    [
                                                     x['n1_score'], 
                                                     x['n2_score'],
                                                     x['n3_score'],
                                                     x['n4_score'],
                                                     x['n5_score'],
                                                     x['n6_score'],
                                                     x['n7_score'],
                                                     x['n8_score'],
                                                     x['n9_score'],
                                                     x['n10_score'],
                                                     x['n11_score'],
                                                     x['n12_score'],
                                                     x['n13_score'],
                                                     x['n14_score']
                                                    ]), axis=1)

    
        
    # List the failure explanation - this is used to apply deficiencies in CO
    df['failure_explanation'] = df.apply(lambda x: vm.explain_failure(x['ssn_match'],
                                                                      x['dob_match'],
                                                                      x['name_match']), axis=1)

    # Convert the failure explanation to a numeric
    df['failure_explanation_numeric'] = df.apply(lambda x: vm.convert_failure_explanation_to_number(x['failure_explanation']), axis=1)

    # Verify the records
    df['verified'] = df.apply(lambda x: vm.verify_record([
                                                          x['full_name_check_value'], 
                                                          x['ssn_score'],
                                                          x['dob_score'],
                                                          x['n1_score'], 
                                                          x['n2_score'],
                                                          x['n3_score'],
                                                          x['n4_score'],
                                                          x['n5_score'],
                                                          x['n6_score'],
                                                          x['n7_score'],
                                                          x['n8_score'],
                                                          x['n9_score'],
                                                          x['n10_score'],
                                                          x['n11_score'],
                                                          x['n12_score'],
                                                          x['n13_score'],
                                                          x['n14_score'],
                                                          x['ssn_match'],
                                                          x['dob_match'],
                                                          x['name_match'],
                                                          x['failure_explanation_numeric'],
                                                          x['last_name_check_value']
                                                         ]), axis=1)

    # Determine if a review is needed on a record
    df['review'] = df.apply(lambda x: vm.determine_review_type(x['full_name_check_value'], 
                                                               x['verified'],
                                                                [
                                                                 x['n1_score'], 
                                                                 x['n2_score'],
                                                                 x['n3_score'],
                                                                 x['n4_score'],
                                                                 x['n5_score'],
                                                                 x['n6_score'],
                                                                 x['n7_score'],
                                                                 x['n8_score'],
                                                                 x['n9_score'],
                                                                 x['n10_score'],
                                                                 x['n11_score'],
                                                                 x['n12_score'],
                                                                 x['n13_score'],
                                                                 x['n14_score']
                                                                ]), axis=1)

    # Create a sent to tlo on date
    df['sent_to_tlo_on'] = df.apply(lambda x: get_tlo_send_date(), axis=1)

    ##
    # Save the results
    ##

    print("{} - Saving the results".format(datetime.now()))



    # Export the results to a CSV file
    df.to_csv(report_file, sep=',', encoding='utf-8')

    ##
    # Clean Up
    ##

    # Move the file to today's folder
    shutil.move(file_to_analyze, report_path)

    print("{} - Report generation complete and the report is ready for review.\n".format(datetime.now()))


def main():
    file_to_process = sys.argv[1]
    type_of_file = sys.argv[2]
    process_tlo_file(file_to_process, type_of_file)


if __name__ == '__main__':
    main()