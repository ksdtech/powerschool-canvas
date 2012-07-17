#!/usr/bin/python
# read in file convert to canvas format

import csv
import re

terms = { }
with open('py_students.csv', 'wb') as ef:
  students = csv.DictWriter(ef,
    ['user_id', 'login_id', 'password', 'first_name', 'last_name', 'email', 'status'])
  # students.writeheader()
  ef.write(','.join(students.fieldnames))
  ef.write("\n")

  with open('students.txt', 'rb') as infile:
    course_ids = { }
    reader = csv.DictReader(infile, delimiter="\t", quotechar="^")
    # like ruby's CSV symbol_converter
    reader.fieldnames = [re.sub(' ', '_', re.sub('^\[[^\]]+\]', '', x.lower())) for x in reader.fieldnames]

    for row in reader:
      first_name = row['nickname']
      if len(first_name) == 0:
        first_name = row['first_name']
      srow = { }
      srow['user_id']    = 'U' + row['student_number']
      srow['login_id']   = row['network_id']
      srow['password']   = row['network_password']
      srow['first_name'] = first_name
      srow['last_name']  = row['last_name']
      srow['email']      = row['network_id'] + '@kentstudents.org'
      srow['status']     = 'active'
      students.writerow(srow)
