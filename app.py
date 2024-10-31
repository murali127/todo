from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Path to the tasks JSON file
TASKS_FILE = 'tasks.json'

def read_tasks():
    """Read tasks from the JSON file."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

def write_tasks(tasks):
    """Write tasks to the JSON file."""
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

@app.route('/')
def index():
    """Render the index page with tasks."""
    tasks = read_tasks()
    # To prevent undefined errors, set current_user as None if not logged in
    current_user = {'username': 'Guest'}  # Change this based on your authentication logic
    return render_template('index.html', tasks=tasks, current_user=current_user)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task."""
    task_content = request.form.get('task')
    tasks = read_tasks()
    tasks.append({'content': task_content})
    write_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    """Delete a task by its ID."""
    tasks = read_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        write_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
