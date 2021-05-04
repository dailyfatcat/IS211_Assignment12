'''Import statements'''
import sqlite3
import click
from flask import Flask, redirect, session, url_for, request, flash
from markupsafe import escape
from flask import current_app, g, render_template
from flask.cli import with_appcontext
from db import get_db, init_db

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'hw13.db'
MESSAGE = ""

@app.route('/')
def index():
    '''Redirect to the login page if going to /'''
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Show the login page'''
    return(render_template("login.html"))


@app.route('/validate', methods=['POST', 'GET'])
def validate():
    '''Part II Teacher Login'''
    username = request.form['username']
    password = request.form['password']
    if username == "admin" and password == "password":
        '''Encountered difficulties with the session, 
        after testing I was not able to deteremine 
        how to make the sessions work if the user did not enter something
        at the login page, current sessions is not working
        Pages will open if browsed to regardless of login'''
        session['username'] = request.form['username']
        return(redirect(url_for("dashboard")))
    else:
        return(redirect(url_for("login")))


@app.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    '''Part III Dashboard: View students and quizzes in the class'''
    db = get_db()
    student_results = g.db.execute("SELECT * FROM students").fetchall()
    quiz_results = g.db.execute("SELECT * FROM quizzes").fetchall()
    return render_template('dashboard.html', student=student_results, quiz=quiz_results)


@app.route('/student/<id>', methods=["POST", "GET"])
def getstudent(id):
    '''Part VI View Quiz Results'''
    db = get_db()
    quiz_scores = None
    #Optional Part: Expand the Results Output
    quiz_scores = g.db.execute("SELECT name, subject, score, date FROM results "
                               "INNER JOIN  students on results.student_id == students.student_id "
                               "INNER JOIN quizzes on results.quiz_id == quizzes.quiz_id "
                               "WHERE students.student_id==(?)", (id,)).fetchall()
    if quiz_scores:
        return render_template("view_student_results.html", scores=quiz_scores, message="Quiz Scores Are:")
    else:
        return render_template("view_student_results.html", message="No Results")


@app.route('/results/add', methods=["POST", "GET"])
def addscore():
    '''Part VII: Add a Student’s Quiz Result (initial page)'''
    db = get_db()
    student_results = g.db.execute("SELECT * FROM students").fetchall()
    quiz_results = g.db.execute("SELECT * FROM quizzes").fetchall()
    return (render_template('results_add.html', student=student_results, quiz=quiz_results))


@app.route('/results_add', methods=["POST", "GET"])
def add_Score():
    '''Part VII: Add a Student’s Quiz Result (function that submit button calls)'''
    error = None
    try:
        db = get_db()
        studentid = request.form.get("Student")
        quizid = request.form.get("Quiz")
        grade = request.form.get("score")
        db.execute("INSERT INTO results (quiz_id, student_id, score) VALUES (?,?,?)", (quizid, studentid, grade,))
        db.commit()
        return redirect(url_for("dashboard"))
    except:
        flash('Unable to add Quiz Results')
        return render_template('results_add.html', error=error)

@app.route('/student/add', methods=["POST", "GET"])
def add_student():
    '''Part IV Add students to the class'''
    db = get_db()
    #No error or issues for when first retrieving the page
    error = None
    if request.method == "GET":
        return render_template('add_student.html')
    #Try to add the student or display and error message if unable to
    try:
        studentname = request.form.get("stuname")
        db.execute("INSERT INTO students (name) VALUES (?)", (studentname,))
        db.commit()
        return (redirect(url_for("dashboard")))
    except:
        flash('Unable to add student')
        return render_template('add_student.html', error=error)


@app.route('/quiz/add', methods=["POST", "GET"])
def add_quiz():
    '''Part VI View Quiz Results'''
    db = get_db()
    # No error or issues for when first retrieving the page
    error = None
    if request.method == "GET":
        return render_template('add_quiz.html')
    # Try to add the quiz or display and error message if unable to
    try:
        quizsub = request.form.get('subject')
        quizform = request.form.get('date')
        quizqa = request.form.get('numquestions')
        db.execute("INSERT INTO quizzes (subject, date, numquestions) VALUES (?,?,?)", (quizsub, quizform, quizqa,))
        db.commit()
        return (redirect(url_for("dashboard")))
    except:
        flash('Unable to add Quiz')
        return render_template('add_quiz.html', error=error)


if __name__ == '__main__':
    app.run()

