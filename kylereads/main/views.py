from flask import render_template, redirect, url_for, flash
from . import main
from flask.ext.login import current_user
from .forms import AddReadingSessionForm
from ..flash_errors import flash_errors
from ..models import ReadingSession, Title
from .. import db

@main.route('/')
def root():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return render_template('welcome.html')

@main.route('/add/session', methods = ['GET', 'POST'])
def add_reading_session():
    form = AddReadingSessionForm()
    if form.validate_on_submit():
        title = Title(title = form.title.data,
                      author = form.author.data,
                      genre = form.genre.data)
        session = ReadingSession(user = current_user,
                                 title = title,
                                 pp = form.pp.data,
                                 date = form.date.data,
                                 completed = form.completed.data)
        db.session.add_all([title, session])
        flash('Added your session!')
        return redirect(url_for('main.root'))
    else:
        flash_errors(form)
    return render_template('add_session.html', form = form)
