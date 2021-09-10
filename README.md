# covidator

covidator is a tool to validate COVID test results.

## Setup

Install [pdftotext](https://www.xpdfreader.com).

Create the list of expected patients in `patients.txt` as follows:

```
covidator $ cat patients.txt 
Jane Appleseed
Johnny Appleseed
```

Dump the test results in a directory called `results` as follows (file names don't matter):
```
covidator $ ls results/
test-result-2.pdf test-result.pdf
```

## Sample runs

### Person missing test
```
covidator $ python3 ./covidator.py 
Found a valid test result for Jane Appleseed in test-result-2.pdf

The following patients are missing test results:
 * Johnny Appleseed
```

### All negative
```
covidator $ python3 ./covidator.py 
Found a valid test result for Jane Appleseed in test-result.pdf
Found a valid test result for Johnny Appleseed in test-result-2.pdf

All 2 patients have been tested
```

### Invalid results
Those could be positive results, results outside the testing window, etc.
```
covidator $ python3 ./covidator.py 
No valid test results in test-result.pdf
No valid test results in test-result-2.pdf

The following patients are missing test results:
 * Jane Appleseed
 * Johnny Appleseed
```
