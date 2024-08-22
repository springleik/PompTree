# PompTree
Python3 code generator _PompTree.py_ randomly creates JSON test cases, as described at http://www.williamsonic.com/CompTree/index.html. Branch nodes are created according to parameters set inside the program, while leaf nodes are created according to the text file _Pleaf.txt_. Everything is adjustable, so the output can be steered and constrained according to your needs. Leaf values are pulled line-by-line from the leaf file, but don't have to be simple types. The leaf file can also contain valid composite structures if each structure is on one line, which are then placed in arrays and dictionaries in the output. Console output can be redirected to a JSON file for further processing.

Also included is a Python3 program _CompTree.py_ which performs an asymmetric directional tree comparison on two JSON files. The files are loaded into memory using Python's _json_ library, by invoking the program on a command line with two arguments representing the reference file and the test file. They are then traversed by recursive descent to check for equality, by the following rules:

* Any dictionary in the test file must have all of the keys in the corresponding dictionary in the reference file.
    * Order is ignored. Dictionaries in the files being compared can have a completely different ordering, and still test as equal.
    * Additional keys in the test file are ignored.
* Any array in the test file must have at least as many elements as the corresponding array in the reference file.
    * Order is maintained and must match, up to the last element in the reference file.
    * Additional array elements in the test file are ignored.
* Each value in a dictionary in the reference file must be equal to the corresponding value in the test file, according to these rules.
* Each element in an array in the reference file must be equal to the corresponding element in the test file, according to these rules.
* Integers must have the same value and sign.
* Floats must have the same value, sign, and exponent.
    * Floats with the value Infinity in the reference file must have a corresponding Infinity in the test file. Sign is not considered in this comparison.
    * Floats with the value NaN in the reference file must have a corresponding NaN in the test file.
* Booleans must either be both True, or both False.
* Text strings must be an exact case-sensitive match, including white space and escape characters inside the string.
    * White space outside of text strings is ignored. The two files being compared can have a completely different formatting in terms of white space, and still test as equal.
* Null values in the reference file must have a corresponding Null value in the test file.

Performing a directional comparison is important when comparing test outputs with reference files, so that the test files can include additional comments, annotation, and instrumentation. Additionally, items you don't want to compare (timestamps, sequence numbers that change often, analog values such as voltage or temperature, etc.) can be ignored in the comparison by removing them from the reference file. The test file can then have varying values for these items and still be considered as equal, in order to pass a regression test for instance. An interesting question is whether to include version info for the software under test. If you leave version info in, then you'll have to touch the reference file each time you test a new version. If you actually need an exact match in both directions, simply test the files twice, reversing their order so both are evaluated as test files. If both comparisons are True, then both files have exactly the same dictionary keys and array elements.

Some simple JSON files _a.json_ and _b.json_ are placed here to show how the comparison works. Either can be used as test or reference. If the same file is both test and reference, then the comparison will be True. The file _a.json_ has an extra array element, and the file _b.json_ has an extra dictionary key. So any comparison involving both files should be False. File comparison output to _stdout_ is either an empty JSON array if the files are a match, or a JSON array populated with error objects if the files don't match. Error objects contain a description of each error, and the path from the root node to the error location. An errorlevel is also returned which is zero if files match. A non-zero errorlevel is returned if the files mismatch, or if the input files don't both contain valid JSON text. The CompareTree program includes a _main_() function and is set up to be imported as a library if you just want to use the comparison function. Several utility functions are also included.

* _locateKey(key, data)_ Locate _key_ in _data_, return a generator for _key_'s value
* _locatePair(key, value, data)_ Locate _key_/_value_ pair in _data_, return a generator for the containing object
* _treeCompare(ref, tst, error = [])_ Recursively test JSON tree structures in _ref_ and _tst_ for equality. Return a true/false result, and optionally append details of each mismatch to the _error_ list.
* _locateTree(sub, data)_ Locate instances of subtree _sub_, traversing containing tree _data_ by recursive descent. Returns a list of matches found

Python3 program _CompareTest.py_ imports these functions, to show examples of their use. The console output from this program is a JSON array, which can be compared to previous results for regression testing. Typical results are saved in files _CompareRef.json_ and _CompareTest.json_.
