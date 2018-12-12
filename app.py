from datetime import datetime

from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, RadioField
from wtforms.validators import Length, InputRequired

import db

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def teardown_request(exception):
    db.disconnect()


class GetCamperForm(FlaskForm):
    get_camper = IntegerField('Swim Number', validators=[InputRequired(message='Swim Number Required')])
    submit = SubmitField('Find Camper')


@app.route('/', methods=['GET', 'POST'])
def index():
    get_form = GetCamperForm()
    if get_form.validate_on_submit():
        camper_exists = True
        camper_id = db.load_camper(get_form.get_camper.data)

        if camper_id is None:
            camper_exists = False
            flash("Cannot find Camper")

        else:
            flash("Camper Found")
            return redirect(url_for('camper_details', id=camper_id[0]))
    return render_template("index.html", form=get_form)


class NewCamperForm(FlaskForm):
    add_name = StringField('Name', validators=[InputRequired(message='Name Required'), Length(max=20)])
    add_swim_number = IntegerField('Swim Number', validators=[InputRequired(message='Swim Number Required')])
    add_prompt = StringField('Prompt', validators=[Length(max=20)])
    submit = SubmitField('Add Camper')


@app.route('/add-camper', methods=['GET', 'POST'])
def add_camper():
    camper_form = NewCamperForm()
    session = db.get_active_session()
    if camper_form.validate_on_submit():
        rowcount = db.add_camper(camper_form.add_name.data,
                                 camper_form.add_swim_number.data,
                                 camper_form.add_prompt.data,
                                 session[0])
        if rowcount == 1:
            flash('{}:Camper added Successfully'.format(camper_form.add_name.data))
            return redirect(url_for('index'))
        else:
            flash('Creation Failed')
    return render_template('add_camper.html', form=camper_form, mode='create')


class TransactionForm(FlaskForm):
    trans_type = SelectField("Transaction Type",
                             choices=[(1, 'Deposit'), (2, 'Concessions'), (3, 'Shirt Shack'), (4, 'Withdrawal')],
                             coerce=int)
    amount = IntegerField("amount", validators=[InputRequired(message='Amount Required')])
    submit = SubmitField('Post Transaction')


@app.route('/camper-details/<id>', methods=['GET', 'POST'])
def camper_details(id):
    camper_info = db.get_camper(id)
    camper_name = camper_info[1]
    swim_number = camper_info[2]
    camper_prompt = camper_info[3]
    camp_session = db.get_session(camper_info[4])[0]
    trans_form = TransactionForm()

    if trans_form.validate_on_submit():
        time = datetime.today()
        rowcount = db.post_transaction(camper_info[0],
                                       time,
                                       trans_form.trans_type.data,
                                       trans_form.amount.data)
        if rowcount == 1:
            flash('Transaction Posted Successfully')
            return redirect(url_for('index'))
        else:
            flash('Transaction Failed')

    return render_template('camper_info.html', form=trans_form, camper_name=camper_name, swim_number=swim_number,
                           camper_prompt=camper_prompt, camp_session=camp_session)


class NewSessionForm(FlaskForm):
    description = StringField('Session Name, Format: (YYYY-#)',
                              validators=[InputRequired(message='Session Name Required'), Length(max=6)])
    submit = SubmitField('Add Session')


class ActiveForm(FlaskForm):
    change_active = RadioField("Make Active", coerce=int)
    submit = SubmitField('Change Activity')


@app.route('/add-session', methods=['GET', 'POST'])
def create_session():
    add_session_form = NewSessionForm()
    if add_session_form.validate_on_submit():
        rowcount = db.add_session(add_session_form.description.data, False)
        if rowcount == 1:
            flash('New Session Added Successfully')
            return redirect(url_for('index'))
        else:
            flash('Transaction Failed')
    return render_template('add_session.html', form=add_session_form)


@app.route('/activate-session', methods=['GET', 'POST'])
def activate_session():
    # Set up the list of options in the Active Form
    change_active_form = ActiveForm()
    choice_list = []
    for session in db.get_sessions():
        choice_list.append((session['id'], session['description']))
    change_active_form.change_active.choices = choice_list

    active_session = db.get_active_session()
    print("ACTIVE SESSION", active_session)

    if change_active_form.validate_on_submit():
        new_active_session = change_active_form.change_active.data
        print("NEW ACTIVE SESSION", new_active_session)

        rowcount = db.change_activity(new_active_session)
        if rowcount == 1:
            flash("Activity Updated")
            return redirect(url_for('index'))
        else:
            flash('Change Failed')

    return render_template('activate_session.html',
                           form=change_active_form,
                           active_session=active_session[1])


if __name__ == '__main__':
    app.run()
