from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_wtf import FlaskForm
# from wtforms.fields import FileField
from wtforms import StringField, SubmitField, SelectField, PasswordField, FloatField, BooleanField
from wtforms.validators import Email, Length, InputRequired, Regexp, EqualTo, NumberRange
# from wtforms.fields.html5 import IntegerField
import db

app = Flask(__name__)


@app.before_request
def before_request():
    db.connect()

@app.teardown_request
def teardown_request(exception):
    db.disconnect()

@app.route('/')
def hello_world():
    return render_template("index.html")

class NewCamperForm(FlaskForm):
    add_name = StringField('name', validators=[InputRequired(message='Name Required'), Length(max=20)])
    add_prompt = StringField('prompt', validators=[InputRequired(message='Prompt Required'), Length(max=20)])

class NewSessionForm(FlaskForm):
    add_description = StringField('description', validators=[InputRequired(message='Session Description Required'),Length(max=6)])
    set_active = BooleanField()

@app.route('/add-camper')
def add_camper():
    account_form = NewCamperForm()
    if account_form.validate_on_submit():
            rowcount=db.add_camper(
                account_form.name.data,
                account_form.prompr.data)
            if rowcount == 1:
                flash('{}:Camper added Successfully'.format(account_form.name.data))
            else:
                flash('Creation Failed')
    return render_template(add_camper.html, form=account_form, mode='create')

if __name__ == '__main__':
    app.run()
