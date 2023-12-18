# Maneja la lista de tares
from flask import Blueprint, render_template,redirect, url_for,request,g

from todor.auth import login_required

from .models import Todo, User
from todor import db



bp = Blueprint("todo", __name__, url_prefix="/todo")

@bp.route('/list')
@login_required
def index():
    todos = Todo.query.all()
    return render_template("todo/index.html", todos = todos)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']

        todo = Todo(g.user.id, title, desc)

        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo.index'))
    return render_template('todo/create.html')

# creamos una funsion para editar 
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return todo

@bp.route('/update/<int:id>', methods = ('GET', 'POST'))
@login_required
def update(id):

    todo = get_todo(id)

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.state = True if request.form.get('state') == 'on' else False

        db.session.commit()

        return redirect(url_for('todo.index'))
    return render_template('todo/update.html' , todo = todo)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))