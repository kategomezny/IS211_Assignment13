CREATE TABLE IF NOT EXISTS Student (

    student_id  INTEGER PRIMARY KEY AUTOINCREMENT,

    first_name TEXT,

    last_name TEXT

);

CREATE TABLE IF NOT EXISTS Quiz (

    Quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,

    Subject TEXT,

    Number_of_questions INTEGER,

    Date TEXT

);

CREATE TABLE IF NOT EXISTS Results (

    Record_id INTEGER PRIMARY KEY AUTOINCREMENT,

    Student_id INTEGER,

    Quiz_id INTEGER,

    Score INTEGER

);

