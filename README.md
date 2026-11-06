# Vibhor-s-student-performanmce-predictor-mini-project
# Student Performance Predictor

A Python program that predicts a student's final marks from study hours,
attendance, previous marks and assignment completion.

## Features
- Add a student and get predicted marks, grade, result and advice
- Data stored in a CSV file (`students.csv`)
- View all students, summary statistics, and save a text report

## Python concepts used
Variables, data types, type conversion, input/output, if-else, loops,
break/continue/pass, functions, lambda, strings, lists, tuples, sets,
dictionaries, list comprehension, regex, classes, constructors, destructors,
inheritance, polymorphism, encapsulation, file handling (text and CSV),
exception handling.

## How to run
```
python student_predictor.py
```
No extra libraries needed.

## How prediction works
predicted = 0.45 x previous marks + 0.20 x attendance
          + 0.20 x assignments + 1.9 x study hours (capped at 100)
A student with 40 or more marks is predicted to pass.

## Future improvements
- Train a machine learning model on real data
- Build a GUI or web page

## Author
Your Name - PRN - Branch
