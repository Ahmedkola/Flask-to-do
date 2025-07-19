from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from app.models import Task
from app import db

task_bp = Blueprint('task', __name__)

@task_bp.route('/view_tasks', methods=['GET', 'POST'])
def view_tasks():
    if 'user' not in session:  # ✅ fix: check 'user' key in session dict
        flash('You need to log in first.', 'warning')
        return redirect(url_for('auth.login'))
    
    tasks = Task.query.all()
    return render_template('task.html', tasks=tasks)

@task_bp.route('/add_task', methods=['POST'])
def add_task():
    if 'user' not in session:  # ✅ same fix here
        return redirect(url_for('auth.login'))

    title = request.form.get('title')
    if title:
        new_task = Task(title=title, status='pending')
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')

    return redirect(url_for('task.view_tasks'))

@task_bp.route('/toggle_task/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    task = Task.query.get(task_id)  # ✅ fix typo: .get not .grt

    if task:
        if task.status == 'pending':
            task.status = 'ongoing'
        elif task.status == 'ongoing':
            task.status = 'completed'
        else:
            task.status = 'pending'

        db.session.commit()  # ✅ Only commit if task exists

    return redirect(url_for('task.view_tasks'))

@task_bp.route('/clear', methods=['POST'])
def clear_task():
    Task.query.delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')
    return redirect(url_for('task.view_tasks'))
