from flask_wtf import Form
from wtforms import StringField, DateField, IntegerField, SubmitField, BooleanField
from wtforms.validators import InputRequired
import datetime

class AddReadingSessionForm(Form):
    title = StringField(label ='Title', validators = [
                       InputRequired(message = 'Title is required.')])
    date = DateField(label = 'Date',
                     validators = [InputRequired(message = 'Date is required.')],
                     format = '%Y-%m-%d',
                     default = datetime.date.today())
    pp = IntegerField(label = 'Pages',
                      validators = [InputRequired(message = 'Pages is required.')])
    author = StringField(label = 'Author',
                         validators = [InputRequired(message = 'Author is required.')])
    genre = StringField(label = 'Genre',
                        validators = [InputRequired(message = 'Genre is required.')])
    completed = BooleanField(label = 'Completed?', default = 'unchecked')
    submit = SubmitField('Submit')
