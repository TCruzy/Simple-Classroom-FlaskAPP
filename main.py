import string, sqlite3
from flask import Flask, flash, render_template, request, redirect, url_for, make_response
from random import choice
app = Flask(__name__)

# check if given string is a float, use string module to check if it is a float

conn = sqlite3.connect('students.db', check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS students (full_name TEXT, subject TEXT, first_grade FLOAT
            , second_grade FLOAT, third_grade FLOAT, fourth_grade FLOAT, fifth_grade FLOAT)""")
conn.commit()
subjects = ["Python", "Java", "C++", "C", "JavaScript", "HTML", "CSS"]

c.execute("SELECT * FROM students")
if len(c.fetchall()) == 0: # პირველ გაშვებაზე ბაზა თუ ცარიელია სატესტოდ ვამატებ.
    c.execute('''insert into students values ('ნუგო სვიანაძე', ?, 5.0, 3.0, 5.0, 4.0, 5.0)''', (choice(subjects),))
    c.execute('''insert into students values ('გიორგი სტურუა', ?, 5.0, 5.0, 3.0, 4.0, 5.0)''', (choice(subjects),))
    conn.commit()

full_name = ""
sub = ""

@app.route('/<name>/<thesubject>') 
def subject(name, thesubject):
    global full_name, sub
    c.execute('''select * from students where full_name = ? and subject = ?''', (name, thesubject))
    for row in c.fetchall():
        name = row[0]
        thesubject = row[1]
    full_name = name
    sub = thesubject
    return render_template('subject.html', name=name, thesubject=thesubject)
@app.route('/result', methods=['POST', 'GET']) 
def result():
    global name, subject
    if request.method == 'POST':
        if ('.' not in str(request.form['ex1']) and not str(request.form['ex1']).isdigit()) or ('.' not in str(request.form['ex2']) and not str(request.form['ex2']).isdigit()) or ('.' not in str(request.form['ex3']) and not str(request.form['ex3']).isdigit()) or ('.' not in str(request.form['ex4']) and not str(request.form['ex4']).isdigit()) or ('.' not in str(request.form['ex5']) and not str(request.form['ex5']).isdigit()):
            error = "Please enter Correct numbers"
            return render_template('subject.html', error=error,thesubject=sub, name=full_name)
        result = request.form
        ex1 = float(request.form['ex1'])
        ex2 = float(request.form['ex2'])  
        ex3 = float(request.form['ex3'])
        ex4 = float(request.form['ex4'])
        ex5 = float(request.form['ex5'])
        avg = (ex1 + ex2 + ex3 + ex4 + ex5) / 5
        sum = ex1 + ex2 + ex3 + ex4 + ex5
        min_score = 10.5
        if ex1 > 5 or ex1 < 1 or ex2 > 5 or ex2 < 1 or ex3 > 5 or ex3 < 1 or ex4 > 5 or ex4 < 1 or ex5 > 5 or ex5 < 1:
            error = "Please enter a number between 1 and 5"
            return render_template('subject.html', error=error,thesubject=sub, name=full_name)
        if sum < min_score:
            c.execute('''update students set first_grade = ?, second_grade = ?, third_grade = ?, fourth_grade = ?, fifth_grade = ? where full_name = ? and subject = ?''', (ex1, ex2, ex3, ex4, ex5, full_name, sub))
            conn.commit()
            status = "No"
            return render_template('table.html', status=status, avg=avg, sum=sum, result=result, name=full_name, thesubject=sub)
        elif sum >= min_score:
            c.execute('''update students set first_grade = ?, second_grade = ?, third_grade = ?, fourth_grade = ?, fifth_grade = ? where full_name = ? and subject = ?''', (ex1, ex2, ex3, ex4, ex5, full_name, sub))
            conn.commit()
            status = "Yes"
            return render_template('table.html', status=status, avg=avg, sum=sum, result=result, name=full_name, thesubject=sub)

@app.route('/')
def students():
    students = {"name" : [], "subject" : [], "first_grade" : [], "second_grade" : [], "third_grade" : [], "fourth_grade" : [], "fifth_grade" : []}
    c.execute("SELECT * FROM students")
    for row in c.fetchall():
        students["name"].append(row[0])
        students["subject"].append(row[1])
        students["first_grade"].append(row[2])
        students["second_grade"].append(row[3])
        students["third_grade"].append(row[4])
        students["fourth_grade"].append(row[5])
        students["fifth_grade"].append(row[6])
    return render_template('students.html', students=students)


if __name__ == '__main__':
    app.run(debug=True)