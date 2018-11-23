import sqlite3 as lite
from flask import Flask, request,  redirect, url_for, render_template, flash, g
from contextlib import closing
""" keep track of students that are enrolled in a 
class, and the score they have received on quizzes in the class"""

DATABASE = 'hw13.db'
SECRET_KEY = '@\x96\xe4.\x1d\xe9M`\xe8C\x8e?\x17:\x1ee\xafBm^u-\xb4z'


app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return lite.connect(app.config['DATABASE'])


def init_db():

        with closing(connect_db()) as db:
            with app.open_resource('schema.sql',mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
           
        con=lite.connect('hw13.db')
        cur = con.cursor() 
        cur.execute('''INSERT INTO Student(first_name, last_name)
                  VALUES('John','Smith')''')
        cur.execute('''INSERT INTO Quiz(Subject, Number_of_questions, Date)
                  VALUES('Python Basics', 5, 'February 5th, 2015' )''')
        cur.execute('''INSERT INTO Results(Student_id, Quiz_id, Score)
                  VALUES(1, 1, 85)''')

        
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
    con = lite.connect('hw13.db')
 

@app.route('/')
def index():
    return redirect(url_for('login'))
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error= "Invalid username or password.   Please try again"
        else:
            return redirect('/dashboard')
    return render_template('login.html', error=error)

    
   
@app.route('/dashboard', methods=['GET'])
def dashboard():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT student_id, first_name, last_name FROM Student')
    rows_student= cursor.fetchall()    
    cursor.execute('SELECT Quiz_id, Subject, Number_of_questions, Date FROM Quiz')
    rows_quiz= cursor.fetchall()
    cursor.execute("SELECT R.Record_id, S.first_name ||' '|| S.last_name,  Q.Subject || ' - ' || Q.Date, R.Score FROM Quiz Q, Results R, Student S where R.Student_id=S.student_id and R.Quiz_id=Q.Quiz_ID")
    rows_results= cursor.fetchall()
    return render_template('dashboard.html', student=rows_student, quiz=rows_quiz, results=rows_results)


@app.route('/student/add', methods=['GET','POST'])
def student_add():
    if request.method == 'GET':
        return render_template('studentadd.html')
    elif request.method == 'POST':
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Student (first_name, last_name) values ('" + request.form['first_name'] + "', '" + request.form['last_name'] + "')" )
        conn.commit()
        flash('New student has been added sucessfully')
        return redirect(url_for('dashboard'))

      
@app.route('/quiz/add', methods=['GET', 'POST'])
def quiz_add():
    if request.method == 'GET':
        return render_template('quizadd.html')
    elif request.method == 'POST':
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO Quiz (Subject, Number_of_questions, Date) values (?, ?, ?)',
                         [request.form['Subject'], request.form['Number_of_questions'], request.form['Date']])
        conn.commit()
        flash('New quiz has been added sucessfully')
        return redirect('/dashboard')
    
    
@app.route('/results/add', methods=['GET', 'POST'])
def results_add():
    if request.method == 'GET':
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT Quiz_id, Subject, Date FROM Quiz')
        rows_quizzes= cur.fetchall()
        cur.execute('SELECT student_id, first_name, last_name from Student')
        rows_students= cur.fetchall()
        return render_template('resultsadd.html', student=rows_students, quiz=rows_quizzes)
    elif request.method == 'POST':
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO Results (student_id, Quiz_id, Score) values "
                     "(?, ?, ?)", (request.form['Student'],
                                   request.form['Quiz'], request.form['Grade']))
        conn.commit()
        flash("Quiz results has been updated")
        return redirect('/dashboard')
    else:
        flash("Results could not been updated")
        return redirect('/results/add')

if __name__ == '__main__':
    app.run(debug=True)
