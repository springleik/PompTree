#!/usr/bin/env python3
# CompTest.py imports CompTree.py as a
# library, to verify correct operation
# M. Williamsen  26 November 2023
import json, sys, datetime, os
import CompTree as ct

# --------------------------------------------
# open test input and output files
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
    
try:
    outFileName = 'Tst.json'
    outFile = open(outFileName, 'w')
except IOError as e:
    print ('Failed to open output file: {}'.format(outFileName), file = sys.stderr)
    sys.exit(-1)

# place timestamp at start of file
print ('{{"timestamp":"{}"'.format(datetime.datetime.now()), file = outFile)

# --------------------------------------------
# treeCompare
errors = []
ct.treeCompare(tstData, refData, errors)
print (',"treeCompare1":{}'.format(json.dumps(errors)), file = outFile)

errors = []
ct.treeCompare(refData, tstData, errors)
print (',"treeCompare2":{}'.format(json.dumps(errors)), file = outFile)

errors = []
ct.treeCompare([], tstData, errors)
print (',"treeCompare3":{}'.format(json.dumps(errors)), file = outFile)

errors = []
ct.treeCompare({}, tstData, errors)
print (',"treeCompare4":{}'.format(json.dumps(errors)), file = outFile)

# --------------------------------------------
# open test input files for following tests
try:
    tstFileName = 'TestFiles/cc.json'
    with open(tstFileName, 'r') as tstFile:
        tstData = json.load(tstFile)
except ValueError as e:
    print ('Tst file {} is not valid JSON'.format(tstFileName), file = sys.stderr)
    sys.exit (-1)

# --------------------------------------------
# locateKey
rslt = ct.locateKey('one', tstData)
print (',"locateKey1":{}'.format(json.dumps(list(rslt))), file = outFile)

rslt = ct.locateKey('five', tstData)
print (',"locateKey2":{}'.format(json.dumps(list(rslt))), file = outFile)

# --------------------------------------------
# locatePair
rslt = ct.locatePair('one', 1, tstData)
print (',"locatePair1":{}'.format(json.dumps(list(rslt))), file = outFile)

rslt = ct.locatePair('five', 'aa', tstData)
print (',"locatePair2":{}'.format(json.dumps(list(rslt))), file = outFile)

# --------------------------------------------
# locateTree
sub = {
        "one": 1,
        "two": 22,
        "three": 23
      }
match = []
ct.locateTree(sub, tstData, match)
print (',"locateTree1":{}'.format(json.dumps(list(match))), file = outFile)

sub = {
        "three": 23,
        "four": 25
      }
match = []
ct.locateTree(sub, tstData, match)
print (',"locateTree2":{}'.format(json.dumps(list(match))), file = outFile)

sub = {
        "three": 24,
        "four": 25
      }
match = []
ct.locateTree(sub, tstData, match)
print (',"locateTree3":{}}}'.format(json.dumps(list(match))), file = outFile)

# --------------------------------------------
# Compare test output file with reference file
# Test passes if console shows an empty array
outFile.close()
os.system('python3 CompTree.py Ref.json Tst.json')
