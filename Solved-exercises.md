# Solved Exercises for SQLite3 Database with Faker

This document contains solved exercises based on the SQLite3 database populated with fictional data using the Faker library. The exercises focus on data cleaning and advanced data handling techniques.

## Table of Contents

1. [Exercise 1: Identify Missing Values](#exercise-1-identify-missing-values)
2. [Exercise 2: Impute Missing Data](#exercise-2-impute-missing-data)
3. [Exercise 3: Filter Data](#exercise-3-filter-data)
4. [Exercise 4: Group and Calculate Statistics](#exercise-4-group-and-calculate-statistics)
5. [Exercise 5: Combine Data from Multiple Tables](#exercise-5-combine-data-from-multiple-tables)

---

## Exercise 1: Identify Missing Values

### Objective

Identify all records in the `students`, `grades`, and `attendance` tables that contain missing values (`None`).

### Solution

```python
import sqlite3

# Connect to the database
connection = sqlite3.connect('escuela.db')
cursor = connection.cursor()

# Identify missing values in the students table
cursor.execute("SELECT * FROM alumnos WHERE edad IS NULL OR correo IS NULL")
students_missing = cursor.fetchall()
print("Students with missing values:", students_missing)

# Identify missing values in the grades table
cursor.execute("SELECT * FROM calificaciones WHERE calificacion IS NULL")
grades_missing = cursor.fetchall()
print("Grades with missing values:", grades_missing)

# Identify missing values in the attendance table
cursor.execute("SELECT * FROM asistencias WHERE asistencias IS NULL")
attendance_missing = cursor.fetchall()
print("Attendance records with missing values:", attendance_missing)

connection.close()
```

### Explanation
This script connects to the SQLite database and queries the students, grades, and attendance tables to find any records where the values are missing (i.e., NULL in SQL, represented as None in Python). The results are printed to the console.

## Exercise 2: Impute Missing Data

### Objective
Impute the missing student ages with the median age and replace missing attendance values with 0.

### Solution
```python
import sqlite3
import pandas as pd

# Connect to the database
connection = sqlite3.connect('escuela.db')

# Impute missing values in the students table
df_students = pd.read_sql_query("SELECT * FROM alumnos", connection)
median_age = df_students['edad'].median()
df_students['edad'].fillna(median_age, inplace=True)
df_students.to_sql('alumnos', connection, if_exists='replace', index=False)

# Impute missing values in the attendance table
cursor = connection.cursor()
cursor.execute("UPDATE asistencias SET asistencias = 0 WHERE asistencias IS NULL")
connection.commit()

connection.close()
```

### Explanation
The code uses pandas to load the students table into a DataFrame and fills missing edad (age) values with the median age. It then updates the database with the imputed data. The missing attendance values are replaced with 0 using a SQL UPDATE statement.

## Exercise 3: Filter Data

### Objective
Filter students who have a grade greater than 8 in any course.

### Solution

```python
import sqlite3

# Connect to the database
connection = sqlite3.connect('escuela.db')
cursor = connection.cursor()

cursor.execute('''
SELECT alumnos.nombre, cursos.nombre_curso, calificaciones.calificacion
FROM calificaciones
JOIN alumnos ON calificaciones.alumno_id = alumnos.id
JOIN cursos ON calificaciones.curso_id = cursos.id
WHERE calificaciones.calificacion > 8
''')
results = cursor.fetchall()

for result in results:
    print(result)

connection.close()
```

### Explanation
This script queries the database to find students who have scored more than 8 in any course. It joins the students, courses, and grades tables to retrieve the relevant data.

## Exercise 4: Group and Calculate Statistics

### Objective
Calculate the average grade for each course.

### Solution
```python
import sqlite3

# Connect to the database
connection = sqlite3.connect('escuela.db')
cursor = connection.cursor()

cursor.execute('''
SELECT cursos.nombre_curso, AVG(calificaciones.calificacion) as promedio_calificacion
FROM calificaciones
JOIN cursos ON calificaciones.curso_id = cursos.id
GROUP BY cursos.nombre_curso
''')
averages = cursor.fetchall()

for average in averages:
    print(average)

connection.close()
```

### Explanation
This code calculates the average grade for each course by grouping the grades table by course_id and using the SQL AVG function.

## Exercise 5: Combine Data from Multiple Tables

### Objective
Combine data from the students, courses, and attendance tables to find students with fewer than 5 attendances in any course.

### Solution
```python
import sqlite3

# Connect to the database
connection = sqlite3.connect('escuela.db')
cursor = connection.cursor()

cursor.execute('''
SELECT alumnos.nombre, cursos.nombre_curso, asistencias.asistencias
FROM asistencias
JOIN alumnos ON asistencias.alumno_id = alumnos.id
JOIN cursos ON asistencias.curso_id = cursos.id
WHERE asistencias.asistencias < 5
''')
results = cursor.fetchall()

for result in results:
    print(result)

connection.close()
```

### Explanation
This script finds students with less than 5 attendances in any course by joining the students, courses, and attendance tables.

## Conclusion

These exercises demonstrate how to handle common data cleaning and manipulation tasks using SQLite and Python. The solutions provided can be adapted and expanded for more complex scenarios in real-world applications.

This `Solved-exercises.md` file is designed to be a detailed explanation and solution guide for the exercises related to the SQLite3 database and Faker-generated data. Each exercise includes the objective, the solution code, and an explanation to help understand the steps taken to achieve the solution.
