#!/usr/bin/env python

"""
Script to match COVID test results vs a list of patients
"""

from __future__ import absolute_import, division, print_function
import datetime
import os
import os.path
import pdftotext


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
      if (today - i).strftime('%m/%d/%Y') in result:
         day = today - i
         break
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
   for results_file in os.listdir(results_dir):
      results_file_path = os.path.join(results_dir, results_file)
      with open(results_file_path) as results_file:
         pdf = pdftotext.PDF(results_file)
      for page in pdf:
         patient = validate_result(page, patients)
         if patient:
            patients_tested.add(patient)
   print(patients - patients_tested)


if __name__ == "__main__":
   main()
