#!/usr/bin/env python
# encoding: utf-8
"""
tlo_verification_and_matching.py
Created by Robert Dempsey on 05/18/2015
Updated by Robert Dempsey on 07/29/2015

"""

import pickle


def verify_record(record_scores):
    """
    Given a pandas dataframe with the scores for a record, a record is either verified (1) or non-verified (0)
    :param item: the set of scores for a record
    :return: verification: 0 = non-verified, 1 = verified
    """

    # Reload the trained model
    tlo_classifier_file = "models/tlo_lr_classifier_07.28.15.dat"
    logClassifier = pickle.load(open(tlo_classifier_file, "rb"))

    # Return the prediction
    return logClassifier.predict(record_scores)[0]
    # print(logClassifier.predict(record_scores)[0])



def ssn_match(ssn_score):
    """
    Given an SSN score a record is a match (1) or not a match (0)
    :param ssn_score: the ssn score to test
    :return: match: 0 = not-match, 1 = match 
    """
    if ssn_score == 300:
        return 1
    else:
        return 0


def dob_match(dob_score):
    """
    Given an DOB score a record is either a match (1) or not a match (0)
    :param dob_score: the dob score to test
    :return: match: 0 = not-match, 1 = match 
    """
    if dob_score == 300:
        return 1
    else:
        return 0


def name_match(full_name_check_value, last_name_check_value, name_scores):
    """
    Given all of the name scores, if any of them = 300 then we have a match
    :return: match: 0 = not-match; 1 = match
    """

    if full_name_check_value == 1 or last_name_check_value == 1:
        return 1

    for v in name_scores:
        if v >= 280:
            return 1
    
    return 0


def determine_review_type(full_name_check_value, verified, name_scores):
    """
    Determines the type of review needed for a record given N1 and N2 scores
    Rule 2: If any name score is 280 or above, no review because it's verified
    Rule 2: If 280 > name_score >= 260 => Flag for visual review
    Rule 3: Everything else is flagged for alias review
    :param n1_score:
    :param n2_score:
    :return: review_type
    """
    if full_name_check_value == 1 or verified == 1:
        return ""

    for v in name_scores:
        if v >= 280:
            return ""

    for v in name_scores:
        if 279 >= v >= 260:
            return "VISUAL"

    return ""


def explain_failure(ssn_match_score, dob_match_score, name_match_score):
    """
    Explains the reason for a record failing one or more checks
    """
    reason = ""

    if ssn_match_score == 0:
        reason += "SSN "
    if dob_match_score == 0:
        reason += "DOB "
    if name_match_score == 0:
        reason += "NAME "

    return reason.strip()


def convert_failure_explanation_to_number(failure_explanation):
    """
    Converts the provided failure explanation to a number
    """    
    failure_explanation = failure_explanation.lower()

    if failure_explanation == 'dob':
        return 0
    elif failure_explanation == 'name':
        return 1
    elif failure_explanation == 'ssn dob name':
        return 2
    elif failure_explanation == 'ssn':
        return 3
    elif failure_explanation == 'ssn name':
        return 4
    elif failure_explanation == 'ssn dob':
        return 5
    elif failure_explanation == 'dob name':
        return 6
    else:
        return 0