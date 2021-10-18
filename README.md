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
# Running instructions
## Python Code
### De-identification Phone Information
1- Change to the python directory

2- run ```python deid-Gulay-Ulukaya-DateYear.py id.text DateYear_Gulay_Ulukaya.phi```

In which:

* ```id.text``` contains Patient Notes.

* ```phone.phi``` is the output file that will be created.
### Stats Phone Information

1- change to the python directory

2- run ```python stats.py id.deid id-phi.phrase DateYear_Gulay_Ulukaya.phi ```

In which:

* ```id.deid``` is the gold standard that is category-blind.
* ```id-phi.phrase``` is the gold standard with the categories included.

* ```phone.phi``` is the test file that the stats is run on.
  
    
    ### De-identification Date Information
1- Change to the python directory

2- run ```python deid.py id.text phone.phi```

In which:

* ```id.text``` contains Patient Notes.
* ```date.phi``` is the output file that will be created.
### Stats Date Information
1- change to the python directory

2- run ```python stats.py id.deid id-phi.phrase date.phi ```

In which:

* ```id.deid``` is the gold standard that is category-blind.
* ```id-phi.phrase``` is the gold standard with the categories included.
* ```date.phi``` is the test file that the stats is run on.  
  
  
 ### Stats Result  
 

\==========================

Num of true positives = 415

Num of false positives = 299

Num of false negatives = 1364

Sensitivity/Recall = 0.233

PPV/Specificity = 0.614

\==========================


Total events in 'id-phi.phrase': 1779

\========================================

Categories Present:

Location

DateYear

Date

HCPName

PTName

RelativeProxyName

Phone

Other

PTNameInitial

Age

\========================================






Examining "Location" category.


\==========================

Num of true positives = 7

Num of false positives = 500

Num of false negatives = 360

Sensitivity/Recall = 0.019

PPV/Specificity = 0.355

\==========================


Examining "DateYear" category.


\==========================

Num of true positives = 0

Num of false positives = 505

Num of false negatives = 46

Sensitivity/Recall = 0.0

PPV/Specificity = 0.348

\==========================


Examining "Date" category.


\==========================

Num of true positives = 399

Num of false positives = 302

Num of false negatives = 83

Sensitivity/Recall = 0.828

PPV/Specificity = 0.61

\==========================


Examining "HCPName" category.


\==========================

Num of true positives = 5

Num of false positives = 502

Num of false negatives = 588

Sensitivity/Recall = 0.008

PPV/Specificity = 0.352

\==========================


Examining "PTName" category.


\==========================

Num of true positives = 4

Num of false positives = 503

Num of false negatives = 50

Sensitivity/Recall = 0.074

PPV/Specificity = 0.351

\==========================


Examining "RelativeProxyName" category.


\==========================

Num of true positives = 0

Num of false positives = 505

Num of false negatives = 175

Sensitivity/Recall = 0.0

PPV/Specificity = 0.348

\==========================


Examining "Phone" category.


\==========================

Num of true positives = 0

Num of false positives = 505

Num of false negatives = 53

Sensitivity/Recall = 0.0

PPV/Specificity = 0.348

\==========================


Examining "Other" category.


\==========================

Num of true positives = 0

Num of false positives = 505

Num of false negatives = 3

Sensitivity/Recall = 0.0

PPV/Specificity = 0.348

\==========================


Examining "PTNameInitial" category.


\==========================

Num of true positives = 0

Num of false positives = 505

Num of false negatives = 2

Sensitivity/Recall = 0.0

PPV/Specificity = 0.348

\==========================


Examining "Age" category.


\==========================

Num of true positives = 0

Num of false positives = 505

Num of false negatives = 4

Sensitivity/Recall = 0.0

PPV/Specificity = 0.348

\==========================


### Conclusion  
There are too many false positive data in the result, indicating that our standard for date format matching is not strict enough. But at the same time we want to minimize false negative results. We should have a lot of room for improvement in regular expressions. You can consider filtering through codes other than regular expressions to reduce false positives.
