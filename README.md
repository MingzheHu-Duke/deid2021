- [de-id](#de-id)
- [Prerequisites](#prerequisites)
  - [Python](#python)
  - [Perl](#perl)
- [Running insturctions](#running-insturctions)
  - [Python Code](#python-code)
    - [De-identification](#de-identification)
    - [Stats](#stats)
- [Homework Results](#homework-results)
  - [Code change](#code-change)
  - [Run & test](#run--test)
    - [Results:](#results)
# de-id
Perl and Python code for de-identifying electronic medical records
# Prerequisites
## Python
* Python 3.5.2
## Perl
* Perl 5, Version 28, Subversion 0 (v5.28.0)
# Running insturctions
## Python Code
### De-identification
1- Change to the python directory

2- run ```python deid.py id.text phone.phi```

In which:

* ```id.text``` contains Patient Notes.
* ```phone.phi``` is the output file that will be created.
### Stats
1- change to the python directory

2- run ```python stats.py id.deid id-phi.phrase phone.phi ```

In which:

* ```id.deid``` is the gold standard that is category-blind.
* ```id-phi.phrase``` is the gold standard with the categories included.
* ```phone.phi``` is the test file that the stats is run on.

# Homework Results

de-identify dates

## Code change
modified code for de-identify date information is stored at `./python/deid-chenbin-huang.py`  
Result has many "false positives", because under the current scenario, cannot easily distinguish fractions like "1/3" and data Jan 3rd without some advanced NLP techniques and the date is not stored in the format of "01/03".  

## Run & test
Change to the python directory and   
```
# Run code
python .\deid-chenbin-huang.py .\id.text date.phi
# Test
python stats.py id.deid id-phi.phrase date.phi
```

### Results:
```
==========================

Num of true positives = 439

Num of false positives = 229

Num of false negatives = 1340

Sensitivity/Recall = 0.247

PPV/Specificity = 0.67

==========================


Total events in 'id-phi.phrase': 1779
========================================
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
========================================






Examining "Location" category.


==========================

Num of true positives = 12

Num of false positives = 439

Num of false negatives = 355

Sensitivity/Recall = 0.033

PPV/Specificity = 0.367

==========================


Examining "DateYear" category.


==========================

Num of true positives = 3

Num of false positives = 446

Num of false negatives = 43

Sensitivity/Recall = 0.065

PPV/Specificity = 0.357

==========================


Examining "Date" category.


==========================

Num of true positives = 408

Num of false positives = 232

Num of false negatives = 74

Sensitivity/Recall = 0.846

PPV/Specificity = 0.666

==========================


Examining "HCPName" category.


==========================

Num of true positives = 5

Num of false positives = 443

Num of false negatives = 588

Sensitivity/Recall = 0.008

PPV/Specificity = 0.362

==========================


Examining "PTName" category.


==========================

Num of true positives = 4

Num of false positives = 444

Num of false negatives = 50

Sensitivity/Recall = 0.074

PPV/Specificity = 0.36

==========================


Examining "RelativeProxyName" category.


==========================

Num of true positives = 2

Num of false positives = 446

Num of false negatives = 173

Sensitivity/Recall = 0.011

PPV/Specificity = 0.357

==========================


Examining "Phone" category.


==========================

Num of true positives = 5

Num of false positives = 446

Num of false negatives = 48

Sensitivity/Recall = 0.094

PPV/Specificity = 0.357

==========================


Examining "Other" category.


==========================

Num of true positives = 0

Num of false positives = 446

Num of false negatives = 3

Sensitivity/Recall = 0.0

PPV/Specificity = 0.357

==========================


Examining "PTNameInitial" category.


==========================

Num of true positives = 0

Num of false positives = 446

Num of false negatives = 2

Sensitivity/Recall = 0.0

PPV/Specificity = 0.357

==========================


Examining "Age" category.


==========================

Num of true positives = 0

Num of false positives = 446

Num of false negatives = 4

Sensitivity/Recall = 0.0

PPV/Specificity = 0.357

==========================
```