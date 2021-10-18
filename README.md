# Week 8 Assignment: de-id of DateYear in medical records
I have chosen to find and deidentify DateYear information in the given medical records.
The edited deid.py is now deid-Gulay-Ulukaya-DateYear.py and resulting accuracy statistics (stats-Gulay-Ulukaya-DateYear.txt) can be found under python directory.

Examining "DateYear" category.


==========================

Num of true positives = 46

Num of false positives = 2188

Num of false negatives = 0

Sensitivity/Recall = 1.0

PPV/Specificity = 0.914

==========================

# Method
Developed the following reg-ex year pattern to distinguish years as a four digit number or a two digit number that is not age:
year_pattern = '((19|20)\d{2})|((?<!(age.|.is.))\d{2}(?!.y))' 
Pattern looks for 19xx or 20xx or just the last two digits of the year (xx) such as 96 where the two digit number is not preceded by " is " or "age " or is not succeeded by " y" since it can say "year old", "y\. o\.", "y\.o\.", "yo", "y", "years old", "year-old", "-year-old", "years-old", "-years-old", "years of age", "yrs of age" to indicate age instead of year.

# Prerequisites
## Python
* Python 3.5.2
## Perl
* Perl 5, Version 28, Subversion 0 (v5.28.0)
# Running insturctions
## Python Code
### De-identification
1- Change to the python directory

2- run ```python deid-Gulay-Ulukaya-DateYear.py id.text DateYear_Gulay_Ulukaya.phi```

In which:

* ```id.text``` contains Patient Notes.
* ```DateYear_Gulay_Ulukaya.phi``` is the output file that will be created.
### Stats
1- change to the python directory

2- run ```python stats.py id.deid id-phi.phrase DateYear_Gulay_Ulukaya.phi ```

In which:

* ```id.deid``` is the gold standard that is category-blind.
* ```id-phi.phrase``` is the gold standard with the categories included.
* ```DateYear_Gulay_Ulukaya.phi``` is the test file that the stats is run on.
