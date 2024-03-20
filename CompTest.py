#!/usr/bin/env python3
# CompTest.py imports CompTree.py as a
# library, and verifies correct operation
# M. Williamsen  26 November 2023

import json, sys
import CompTree as ct


# --------------------------------------------
# open input files used for the following tests
try:
    tstFileName = 'TestFiles/cc.json'
    with open(tstFileName, 'r') as tstFile:
        tstData = json.load(tstFile)
except ValueError as e:
    print ('Tst file {} is not valid JSON'.format(tstFileName), file = sys.stderr)
    sys.exit (-1)

try:
    refFileName = 'TestFiles/dd.json'
    with open(refFileName, 'r') as refFile:
        tstData = json.load(refFile)
except ValueError as e:
    print ('Ref file {} is not valid JSON'.format(refFileName), file = sys.stderr)
    sys.exit (-1)

# --------------------------------------------
# locateKey
rslt = ct.locateKey('one', tstData)
print ('[',json.dumps(list(rslt)))
rslt = ct.locateKey('five', tstData)
print (',',json.dumps(list(rslt)))

# --------------------------------------------
# locatePair
rslt = ct.locatePair('one', 1, tstData)
print (',',json.dumps(list(rslt)))
rslt = ct.locatePair('five', 'aa', tstData)
print (',',json.dumps(list(rslt)))

# --------------------------------------------
# locateTree
sub = {
        "one": 1,
        "two": 22,
        "three": 23
      }
match = []
ct.locateTree(sub, tstData, match)
print (',',json.dumps(list(match)))
sub = {
        "three": 23,
        "four": 25
      }
match = []
ct.locateTree(sub, tstData, match)
print (',',json.dumps(list(match)))
sub = {
        "three": 23,
        "four": 26
      }
match = []
ct.locateTree(sub, tstData, match)
print (',',json.dumps(list(match)))

# --------------------------------------------
# open more test files for following tests
try:
    tstFileName = 'TestFiles/aa.json'
    with open(tstFileName, 'r') as tstFile:
        tstData = json.load(tstFile)
except ValueError as e:
    print ('Tst file {} is not valid JSON'.format(tstFileName), file = sys.stderr)
    sys.exit (-1)

try:
    refFileName = 'TestFiles/bb.json'
    with open(refFileName, 'r') as refFile:
        refData = json.load(refFile)
except ValueError as e:
    print ('Ref file {} is not valid JSON'.format(refFileName), file = sys.stderr)
    sys.exit (-1)
    
# --------------------------------------------
# treeCompare
errors = []
ct.treeCompare(tstData, refData, errors)
print (',',json.dumps(errors))
errors = []
ct.treeCompare(refData, tstData, errors)
print (',',json.dumps(errors),']')