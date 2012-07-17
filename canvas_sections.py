#!/usr/bin/python
# read in file convert to canvas format

import csv
import re

# make sections for the coming year
force_year = 22
section_prefix = 'X'

terms = { }
with open('terms.csv', 'rb') as tf:
  reader = csv.DictReader(tf)
  for row in reader:
    term_id = row['term_id']
    terms[term_id] = { }
    terms[term_id]['start_date'] = row['start_date']
    terms[term_id]['end_date'] =  row['end_date']  

with open('py_enrollments.csv', 'wb') as ef:
  teachers = csv.DictWriter(ef,
    ['course_id', 'user_id', 'role', 'section_id', 'status'])
  # teachers.writeheader()
  ef.write(','.join(teachers.fieldnames))
  ef.write("\n")
  
  with open('py_courses.csv', 'wb') as cf:
    courses = csv.DictWriter(cf,
      ['course_id', 'short_name', 'long_name', 'account_id', 'term_id', 'status'])
    # courses.writeheader()
    cf.write(','.join(courses.fieldnames))
    cf.write("\n")

    with open('py_sections.csv', 'wb') as sf:
      sections = csv.DictWriter(sf,
        ['section_id', 'course_id', 'name', 'status', 'start_date', 'end_date'])
      # sections.writeheader()
      sf.write(','.join(sections.fieldnames))
      sf.write("\n")

      with open('sections.txt', 'rb') as infile:
        course_ids = { }
        reader = csv.DictReader(infile, delimiter="\t", quotechar="^")
        # like ruby's CSV symbol_converter
        reader.fieldnames = [re.sub(' ', '_', re.sub('^\[[^\]]+\]', '', x.lower())) for x in reader.fieldnames]

        for row in reader:
          term_id = int(row['termid'])
          if force_year is not None:
            term_id = force_year*100 + (term_id % 100)
          course_id = 'C' + row['course_number'] + '-' + str(term_id)
          term_id   = 'T' + str(term_id)
          if course_id not in course_ids:
            course_parts = row['name'].split()
            short_name = course_parts[0][0:4].upper()
            if re.match('[K1-8]', course_parts[-1]):
              short_name = short_name + course_parts[-1]
            course_ids[course_id] = 1
            crow = { }
            crow['course_id']  = course_id
            crow['short_name'] = short_name
            crow['long_name']  = row['name']
            crow['account_id'] = 'A' + row['schoolid']
            crow['term_id']    = term_id
            crow['status']     = 'active'
            courses.writerow(crow)
          if term_id in terms:
            section_id = section_prefix + row['id']
            srow = { }
            srow['section_id'] = section_id
            srow['course_id']  = course_id
            srow['name']       = 'S' + row['section_number']
            srow['status']     = 'active'
            srow['start_date'] = terms[term_id]['start_date']
            srow['end_date']   = terms[term_id]['end_date']
            sections.writerow(srow)
            trow = { }
            trow['course_id']  = course_id
            trow['user_id']    = 'U' + row['teachernumber']
            trow['role']       = 'teacher'
            trow['section_id'] = section_id
            trow['status']     = 'active'
            teachers.writerow(trow)
          else:
            print "bad term_id %s" % term_id
            break
