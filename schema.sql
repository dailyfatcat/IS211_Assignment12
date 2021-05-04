DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS results;

CREATE TABLE students (
  student_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

CREATE TABLE quizzes (
  quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT NOT NULL,
  date TEXT NOT NULL,
  numquestions INTEGER NOT NULL
);

CREATE TABLE results (
  quiz_id INTEGER,
  student_id INTEGER,
  score INTEGER
);

