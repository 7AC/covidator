#!/usr/bin/env python

"""
Script to match COVID test results vs a list of patients
"""

from __future__ import absolute_import, division, print_function
import datetime
import os
import os.path
import subprocess


def validate_result(result, patients):
   """ Validate a test result"""
   result_patient = None
   for patient in patients:
      if patient in result:
         result_patient = patient
         break
   if not result_patient:
      return None
   today = datetime.date.today()
   day = None
   for i in range(6):
      candidate = today - datetime.timedelta(days=i)
      if candidate.strftime('%m/%d/%Y') in result:
         # Use the earliest date in the file to be safe
         if not day or day > candidate:
            day = candidate
   if not day:
      return None
   if 'Negative' not in result:
      return None
   return result_patient


def main():
   """Main"""
   with open('patients.txt') as patients_file:
      patients = set(patients_file.read().splitlines())
   patients_tested = set()
   results_dir = 'results'
   results_tmp = '/tmp/result.txt'
   for results_file in os.listdir(results_dir):
      results_file_path = os.path.join(results_dir, results_file)
      # This is a workaround for https://github.com/jalan/pdftotext/issues/36
      subprocess.run(['pdftotext', results_file_path, results_tmp], check=True)
      with open(results_tmp) as text:
         patient = validate_result(text.read(), patients)
      if patient:
         print('Found a valid test result for %s in %s' % (patient, results_file))
         patients_tested.add(patient)
   untested = patients - patients_tested
   if untested:
      print('The following patients are missing test results:', untested)
   else:
      print('All %d patients have been tested' % len(patients))


if __name__ == "__main__":
   main()
