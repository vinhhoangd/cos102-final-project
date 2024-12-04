from flask import Flask, render_template, request, redirect, url_for
import csv

app = Flask(__name__)

class Student:
    def __init__(self, student_id, name, age, major, gender):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.major = major
        self.gende = gender

class StudentManager:
    def __init__(self, filename='students.csv'):
        self.filename = filename
        self.students = self.load_students()

    def load_students(self):
        students = []
        try: 
            with open(self.filename, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row: 
                        students.append(Student(*row))
        except FileNotFoundError:
            pass
        return students
    
    def save_students(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for student in self.students:
                writer.writerow([student.student_id, student.name, student.age, student.major, student.major, student.gender])

    def add_student(self, student):
        self.student.append(student)
        self.save_students()

    def search_student(self, search_term):
        return[
            student for student in self.students
            if search_term.lower() in student.name.lower() or student.student_id == search_term
        ]
          
    def update_student(self, student_id, updated_data):
        for student in self.students:
            if student.student_id == student_id:
                student.name = updated_data.get('name', student.name)
                student.age = updated_data.get('age', student.age)
                student.major = updated_data.get('major', student.major)
                student.gender = updated_data.get('gender', student.gender)
        self.save_students()

manager = StudentManager()
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        age = request.form['age']
        major = request.form['major']
        gender = request.form['gender']
        new_student = Student(student_id, name, age, major, gender)
        manager.add_student(new_student)
        return redirect(url_for('home'))
    return render_template('add_student.html')

@app.route('/search', methods=['GET', 'POST'])
def search_student():
    results = []
    if request.method == 'POST':
        search_term = request.form['search_term']
        results = manager.search_student(search_term)
    return render_template('search_student.html', results=results)

@app.route('/modify/<student_id>', methods=['GET', 'POST'])
def modify_student(student_id):
    student = next((s for s in manager.students if s.student_id == student_id), None)
    if request.method == 'POST' and student:
        updated_data = {
            'name': request.form['name'],
            'age': request.form['age'],
            'major': request.form['major'],
            'gender': request.form['gender']
        }
        manager.update_student(student_id, updated_data)
        return redirect(url_for('display_students'))
    return render_template('modify_student.html', student=student)

@app.route('/display')
def display_students():
    return render_template('display_students.html', students=manager.students)

if __name__ == '__main__':
    app.run(debug=True)

