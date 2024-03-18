#!/usr/bin/python3
# TreeCompare.py JSON directional tree comparison
# M. Williamsen  26 November 2023
import json, sys, math

# ---------------- Library Functions ---------------- #
# locate key in data, return generator for value
def locateKey(key, data):
    if isinstance(data, dict):
        if key in data: yield data[key]
        for i, j in data.items():
            for k in locateKey(key, j): yield k
    elif isinstance(data, list):
        for m in data:
            for n in locateKey(key, m): yield n

# --------------------------------------------------- #
# locate key/value pair in data, return generator for containing object
def locatePair(key, value, data):
    if isinstance(data, dict):
        if (key in data) and (data[key] == value): yield data
        for i, j in data.items():
            for k in locatePair(key, value, j): yield k
    elif isinstance(data, list):
        for m in data:
            for n in locatePair(key, value, m): yield n

# --------------------------------------------------- #
# recursively test JSON tree structures for equality
# return a true/false result, and what differed if false
# pass in an error list if you need a detailed report
def treeCompare (ref, tst, error = [], path = []):
    # try to match dictionary keys
    if isinstance (ref, dict) and isinstance (tst, dict):
        if len(tst) < len(ref):
            error.append ({'Not enough keys in dict':len(tst),'path':path})
            return False
        noErrs = True
        for key in ref:
            if key not in tst:
                error.append ({'Missing key':key,'path':path})
                noErrs = False
            elif not treeCompare (ref[key], tst[key], error, path + [key]):
                noErrs = False
        return noErrs

    # try to match list elements
    elif isinstance (ref, list) and isinstance (tst, list):
        if len(tst) < len(ref):
            error.append ({'Not enough items in list':len(tst),'path':path})
            return False
        noErrs = True
        for n, r in enumerate(ref):
            if not treeCompare (r, tst[n], error, path + [n]):
                noErrs = False
        return noErrs

    # try to match simple types
    elif ref is None and tst is None: return True
    elif isinstance (ref, int)   and isinstance (tst, int):  return leafCompare (ref, tst, error, path)
    elif isinstance (ref, str)   and isinstance (tst, str):  return leafCompare (ref, tst, error, path)
    elif isinstance (ref, bool)  and isinstance (tst, bool): return leafCompare (ref, tst, error, path)
    elif isinstance (ref, float) and isinstance (tst, float):
        if math.isnan(ref)   and math.isnan(tst): return True
        elif math.isinf(ref) and math.isinf(tst): return True
        return leafCompare (ref, tst, error, path)

    # this point reached if types are different or unknown
    else: error.append ({'Type error':[str(type(ref)), str(type(tst))],'path':path}); return False

# helper function for treeCompare
def leafCompare (ref, tst, error, path):
    if ref == tst: return True
    error.append ({'Items mismatch':[ref, tst],'path':path})
    return False

# --------------------------------------------------- #
# locate instances of subtree by recursive descent
def locateTree(sub, data, match):
    # check for match at current level
    if treeCompare (sub, data): match.append(data)

    # check for matches beneath
    if isinstance(data, dict):
        for key, value in data.items():
            locateTree (sub, value, match)
    elif isinstance(data, list):
        for value in data:
            locateTree (sub, value, match)

# ---------------- Main Entry Point ---------------- #
def main():
    # check command line args, expect two file names for ref and test file
    args = sys.argv
    refFileName = 'Ref.json'
    tstFileName = 'Tst.json'
    if 2 < len(args):
        refFileName = args[1]
        tstFileName = args[2]
    else:
        print ('Usage: python3 TreeCompare.py Ref.json Tst.json', file = sys.stderr)
        sys.exit (-1)
    # parse json input files
    print ('Ref: {}, Tst: {}'.format(refFileName, tstFileName))
    try:
        with open(refFileName, 'r') as refFile:
            refData = json.load(refFile)
    except ValueError as e:
        print ('Ref file {} is not valid JSON'.format(refFileName), file = sys.stderr)
        sys.exit (-3)
    try:
        with open(tstFileName, 'r') as tstFile:
            tstData = json.load(tstFile)
    except ValueError as e:
        print ('Tst file {} is not valid JSON'.format(tstFileName), file = sys.stderr)
        sys.exit (-4)
    errs = []
    if not treeCompare(refData, tstData, errs):
        print (json.dumps(errs, indent = 2))
        sys.exit(-2)
    print ('Files match.')

# --------------------------------------------------- #
# this doesn't run, when invoked as a library
if __name__ == '__main__':
    main()
    sys.exit(0)
