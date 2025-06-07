from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import db
from app.models import Task

task_bp = Blueprint('tasks', __name__)


@task_bp.route('/')
def view_tasks():       # function to view all the tasks it is default page

    if 'user' not in session:                   # checking if user is present in database or not
        return redirect(url_for('auth.login'))
    
    tasks = Task.query.all()             # Read all the tasks form the database
    return render_template('tasks.html', tasks=tasks)    # Print all the tasks using task.html file


@task_bp.route('/add', methods=["POST"])
# this fn is for adding tasks to database
def add_tasks():

    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    # this will read title from users input if present
    title = request.form.get('title') 

    if title:
        # If title is present then creating a task object (new row with default pending status)
        new_task = Task(title=title, status='pending')

        # add the task into database
        db.session.add(new_task)
        db.session.commit()
        flash('Task added succefully', 'success')

    return redirect(url_for('tasks.view_tasks'))

# code to change the status of any tasks
@task_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):

    task = Task.query.get(task_id) # fetch the task with specific task ids 
    if task:
        if task.status == 'pending':
            task.status = 'working'
        elif task.status == 'working':
            task.status = 'done'
        else:
            task.status = 'done'

        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))


# code to delete all the tasks
@task_bp.route('/clear', methods=["GET","POST"])
def clear_tasks():
    Task.query.delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')
    return redirect(url_for('tasks.view_tasks'))
