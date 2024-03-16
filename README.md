# PompTree
Python code generator, for creating JSON test cases.
As described at http://www.williamsonic.com/CompTree/index.html.
Also includes a Python program _CompareTree.py_ to perform a directional tree comparison on two JSON files. The files are loaded into memory using Python's _json_ library, by invoking the program on a command line with two arguments representing the reference file name and the test file name. They are then traversed by recursive descent to check for equality by the following rules:

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
* Text strings must be an exact match, including white space and escape characters inside the string.
    * White space outside of text strings is ignored. The two files being compared can have a completely different formatting in terms of white space, and still test as equal.
* Null values in the reference file must have a corresponding Null value in the test file.

Performing a directional comparison is important when comparing test outputs with reference files, so that the test files can include additional comments, annotation, and instrumentation. Additionally, items you don't want to compare (timestamps, analog values such as voltage or temperature, etc.) can be ignored in the comparison by removing them from the reference file. The test file can then have varying values for these items and still be considered as equal, in order to pass a regression test for instance. If you actually need an exact match in both directions, simply test the files twice, reversing their order so both are evaluated as test files. If both comparisons are True, then both files have exactly the same dictionary keys and array elements.

Some simple JSON files _a.json_ and _b.json_ are placed here to show how the comparison works. Either can be used as test or reference. If the same file is both test and reference, then the comparison should be True. The file _a.json_ has an extra array element, and the file _b.json_ has an extra dictionary key. So any comparison involving both files should be False.
