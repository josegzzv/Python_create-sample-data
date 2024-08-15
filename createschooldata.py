import sqlite3
import random
from faker import Faker

# Conectar a la base de datos SQLite
conexion = sqlite3.connect('escuela.db')
cursor = conexion.cursor()

# Crear una instancia de Faker
fake = Faker()

# Crear tablas
cursor.execute('''
CREATE TABLE IF NOT EXISTS alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    correo TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_curso TEXT NOT NULL,
    descripcion TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS calificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER,
    curso_id INTEGER,
    calificacion REAL,
    FOREIGN KEY(alumno_id) REFERENCES alumnos(id),
    FOREIGN KEY(curso_id) REFERENCES cursos(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS asistencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumno_id INTEGER,
    curso_id INTEGER,
    asistencias INTEGER,
    FOREIGN KEY(alumno_id) REFERENCES alumnos(id),
    FOREIGN KEY(curso_id) REFERENCES cursos(id)
)
''')

# Poblar la tabla de alumnos
for _ in range(1000):
    nombre = fake.name()
    edad = random.choice([18, 19, 20, 21, 22, None])  # Algunos valores faltantes para edad
    correo = fake.email() if random.random() > 0.1 else None  # Algunos valores faltantes para correo
    cursor.execute('''
    INSERT INTO alumnos (nombre, edad, correo)
    VALUES (?, ?, ?)
    ''', (nombre, edad, correo))

# Poblar la tabla de cursos
nombres_cursos = [f'Curso {i+1}' for i in range(10)]
for nombre_curso in nombres_cursos:
    descripcion = fake.text(max_nb_chars=200)
    cursor.execute('''
    INSERT INTO cursos (nombre_curso, descripcion)
    VALUES (?, ?)
    ''', (nombre_curso, descripcion))

# Obtener IDs generados para alumnos y cursos
cursor.execute('SELECT id FROM alumnos')
alumnos_ids = [row[0] for row in cursor.fetchall()]

cursor.execute('SELECT id FROM cursos')
cursos_ids = [row[0] for row in cursor.fetchall()]

# Poblar la tabla de calificaciones
for _ in range(5000):
    alumno_id = random.choice(alumnos_ids)
    curso_id = random.choice(cursos_ids)
    calificacion = random.choice([random.uniform(0, 10), None])  # Algunos valores faltantes para calificaciones
    cursor.execute('''
    INSERT INTO calificaciones (alumno_id, curso_id, calificacion)
    VALUES (?, ?, ?)
    ''', (alumno_id, curso_id, calificacion))

# Poblar la tabla de asistencias
for _ in range(100000):
    alumno_id = random.choice(alumnos_ids)
    curso_id = random.choice(cursos_ids)
    asistencias = random.choice([random.randint(0, 20), None])  # Algunos valores faltantes para asistencias
    cursor.execute('''
    INSERT INTO asistencias (alumno_id, curso_id, asistencias)
    VALUES (?, ?, ?)
    ''', (alumno_id, curso_id, asistencias))

# Guardar los cambios y cerrar la conexión
conexion.commit()
conexion.close()

print("Base de datos creada y poblada con datos ficticios utilizando sqlite3 y Faker.")
