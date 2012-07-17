#!/usr/bin/python
# read in file convert to canvas format

# Select teachers in PowerSchool DDA, export with these fields,
# Tab-delimited, LF record delimiter:
#
# TeacherNumber
# Network_ID (our custom field for usernames)
# Network_Password (our custom field for passwords)
# First_Name
# Last_Name
# PreferredName
#
# Save as teachers.txt

import csv
import re

terms = { }
with open('py_teachers.csv', 'wb') as ef:
  teachers = csv.DictWriter(ef,
    ['user_id', 'login_id', 'password', 'first_name', 'last_name', 'email', 'status'])
  # teachers.writeheader()
  ef.write(','.join(teachers.fieldnames))
  ef.write("\n")

  with open('teachers.txt', 'rb') as infile:
    course_ids = { }
    reader = csv.DictReader(infile, delimiter="\t", quotechar="^")
    # like ruby's CSV symbol_converter
    reader.fieldnames = [re.sub(' ', '_', re.sub('^\[[^\]]+\]', '', x.lower())) for x in reader.fieldnames]

    for row in reader:
      first_name = row['preferredname']
      if len(first_name) == 0:
        first_name = row['first_name']
      trow = { }
      trow['user_id']    = 'U' + row['teachernumber']
      trow['login_id']   = row['network_id']
      trow['password']   = row['network_password']
      trow['first_name'] = first_name
      trow['last_name']  = row['last_name']
      trow['email']      = row['network_id'] + '@kentstudents.org'
      trow['status']     = 'active'
      teachers.writerow(trow)
