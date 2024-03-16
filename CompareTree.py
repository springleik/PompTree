#!/usr/bin/python3
# TreeCompare.py JSON directional tree comparison
# M. Williamsen  26 November 2023
import json, sys, math

# //////////////// Command Line Args \\\\\\\\\\\\\\\\ #
# check command line args, expect two file names for ref and test file
args = sys.argv
refFileName = 'Ref.json'
tstFileName = 'Tst.json'
if 2 < len(args):
    refFileName = args[1]
    tstFileName = args[2]
else:
    print (' Usage: python3 TreeCompare.py Ref.json Tst.json', file = sys.stderr)
    sys.exit (-1)

# parse json input files
print ('   Ref: {}, Tst: {}'.format(refFileName, tstFileName))
try:
    with open(refFileName, 'r') as refFile:
        refData = json.load(refFile)
except ValueError as e:
    print ('Reference file {} is not valid JSON'.format(refFileName), file = sys.stderr)
    sys.exit (-2)
try:
    with open(tstFileName, 'r') as tstFile:
        tstData = json.load(tstFile)
except ValueError as e:
    print ('Test file {} is not valid JSON'.format(tstFileName), file = sys.stderr)
    sys.exit (-3)

# //////////////// Library Functions \\\\\\\\\\\\\\\\ #
# locate key in data, return generator for values
def locateKey(key, data):
    if isinstance(data, dict):
        if key in data: yield data[key]
        for i, j in data.items():
            for k in locateKey(key, j): yield k
    elif isinstance(data, list):
        for m in data:
            for n in locateKey(key, m): yield n

# locate key/value pair in data, return generator for containing objects
def locatePair(key, value, data):
    if isinstance(data, dict):
        if (key in data) and (data[key] == value): yield data
        for i, j in data.items():
            for k in locatePair(key, value, j): yield k
    elif isinstance(data, list):
        for m in data:
            for n in locatePair(key, value, m): yield n

# helper function for compareTree()
def leafCompare (ref, tst, errs):
    if ref == tst: return True
    errs += 'Items mismatch: {}, {}.'.format(ref, tst)
    return False

# recursively test JSON tree structures for equality
# return a true/false result, and what differed if false
def compareTree (ref, tst, errs, path):
    # try to match dictionary keys
    if isinstance (ref, dict) and isinstance (tst, dict):
        if len(tst) < len(ref):
            errs.append ('Not enough keys in dict: {}.'.format(len(tst)))
            return False
        for key in ref:
            if key not in tst:
                errs.append ('Missing key: {}.'.format(key))
                return False
            elif not compareTree (ref[key], tst[key], errs, path):
                path.insert (0, '"{}"'.format(key))
                return False
        return True

    # try to match list elements
    elif isinstance (ref, list) and isinstance (tst, list):
        if len(tst) < len(ref):
            errs.append ('Not enough items in list: {}.'.format(len(tst)))
            return False
        for n, r in enumerate(ref):
            t = tst[n]
            if not compareTree (r, t, errs, path):
                path.insert (0, '[{}]'.format(n))
                return False
        return True

    # try to match simple types
    elif ref is None and tst is None: return True
    elif isinstance (ref, int)   and isinstance (tst, int):  return leafCompare (ref, tst, errs)
    elif isinstance (ref, str)   and isinstance (tst, str):  return leafCompare (ref, tst, errs)
    elif isinstance (ref, bool)  and isinstance (tst, bool): return leafCompare (ref, tst, errs)
    elif isinstance (ref, float) and isinstance (tst, float):
        if math.isnan(ref)   and math.isnan(tst): return True
        elif math.isinf(ref) and math.isinf(tst): return True
        return leafCompare (ref, tst, errs)

    # this point reached if types are different or unknown
    else: errs.append ('Type error: {}, {}.'.format(type(ref), type(tst))); return False

# locate instances of subtree by recursive descent
def locateTree(sub, data, match):
    # check for match at current level
    if compareTree (sub, data, errs, path):
        match.append(data)

    # check for matches beneath
    if isinstance(data, dict):
        for key, value in data.items():
            locateTree (sub, value, match)
    elif isinstance(data, list):
        for value in data:
            locateTree (sub, value, match)

# //////////////// Main Entry Point \\\\\\\\\\\\\\\\ #
# clear error and path strings, then compare input files
errs = []
path = []
print          (' Match: {}'.format (compareTree (refData, tstData, errs, path)))
if errs: print (' Error: {}'.format (' '.join(errs)))
if path: print ('  Path: {}'.format (' '.join(path)))
