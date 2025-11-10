from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory database (dictionary)
students = {
    1: {"name": "Ali", "age": 20},
    2: {"name": "Sara", "age": 22}
}

# 1️⃣ GET - Retrieve all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# 2️⃣ POST - Add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    new_id = max(students.keys()) + 1 if students else 1
    students[new_id] = {
        "name": data.get("name"),
        "age": data.get("age")
    }
    return jsonify({"message": "Student added", "student": students[new_id]}), 201

# 3️⃣ PUT - Update existing student
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404
    
    data = request.get_json()
    students[student_id]["name"] = data.get("name", students[student_id]["name"])
    students[student_id]["age"] = data.get("age", students[student_id]["age"])
    return jsonify({"message": "Student updated", "student": students[student_id]})

# 4️⃣ DELETE - Remove a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    if student_id not in students:
        return jsonify({"error": "Student not found"}), 404
    deleted_student = students.pop(student_id)
    return jsonify({"message": "Student deleted", "student": deleted_student})

if __name__ == '__main__':
    app.run(debug=True)
