from flask import Flask, request, jsonify, render_template, redirect, url_for
import database

app = Flask(__name__)

database.init_db()

@app.route('/')
def index():
    tasks = database.get_all_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = database.get_all_tasks()
    return jsonify([dict(task) for task in tasks])

@app.route('/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = database.get_task_by_id(task_id)
    if task:
        return jsonify(dict(task))
    return jsonify({"error": "Task not found"}), 404

@app.route('/task', methods=['POST'])
def create_task():
    title = request.form['title'].strip()
    description = request.form['description'].strip()

    database.add_task(title, description)
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    database.toggle_task_status(task_id)
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    database.remove_task(task_id)
    return jsonify({"message": "Task deleted"})

@app.route('/completed')
def completed_tasks():
    tasks = [task for task in database.get_all_tasks() if task["done"]]
    return render_template('index.html', tasks=tasks)

@app.route('/pending')
def pending_tasks():
    tasks = [task for task in database.get_all_tasks() if not task["done"]]
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)