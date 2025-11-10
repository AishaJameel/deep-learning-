from flask import Flask, request, jsonify, render_template_string, redirect, url_for

app = Flask(__name__)

# Dummy data storage
users = []

# HTML Template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask User App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f4f4f9;
        }
        h1 {
            color: #333;
        }
        table {
            width: 50%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        table, th, td {
            border: 1px solid #888;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        form {
            margin-top: 30px;
            background-color: #fff;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 0 8px rgba(0,0,0,0.1);
            width: 300px;
        }
        input[type="text"], input[type="number"] {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            margin-bottom: 10px;
        }
        button {
            padding: 10px 15px;
            background-color: #007BFF;
            border: none;
            color: white;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>

    <h1>👥 User List</h1>

    {% if users %}
    <table>
        <tr>
            <th>Name</th>
            <th>Age</th>
        </tr>
        {% for user in users %}
        <tr>
            <td>{{ user.name }}</td>
            <td>{{ user.age }}</td>
        </tr>
        {% endfor %}
    </table>
    {% else %}
        <p>No users added yet.</p>
    {% endif %}

    <h2>Add New User</h2>
    <form method="POST" action="/add_user">
        <label for="name">Name:</label><br>
        <input type="text" name="name" id="name" required><br>
        
        <label for="age">Age:</label><br>
        <input type="number" name="age" id="age" required><br>
        
        <button type="submit">Add User</button>
    </form>

</body>
</html>
"""

@app.route('/')
def home():
    return "Hello World"

# @app.route('/home')
# def home():
#     return render_template_string(html_template, users=users)

# POST route from HTML form
@app.route('/add_user', methods=['POST'])
def add_user_html():
    name = request.form['name']
    age = request.form['age']
    users.append({'name': name, 'age': age})
    return redirect(url_for('home'))

# API route (JSON-based)
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user_api():
    data = request.get_json()
    users.append(data)
    return jsonify({"message": "User added successfully", "user": data}), 201

if __name__ == '__main__':
    app.run(debug=True)
