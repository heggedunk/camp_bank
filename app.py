from datetime import datetime

from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import Length, InputRequired

import db

app = Flask(__name__)
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
    submit = SubmitField('Create Account')


@app.route('/add-camper', methods=['GET', 'POST'])
def add_camper():
    camper_form = NewCamperForm()
    if camper_form.validate_on_submit():
        rowcount = db.add_camper(camper_form.add_name.data,
                                 camper_form.add_swim_number.data,
                                 camper_form.add_prompt.data)
        if rowcount == 1:
            flash('{}:Camper added Successfully'.format(camper_form.add_name.data))
            return redirect(url_for('camper_details'))
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
    active = BooleanField('Active?')
    Submit = SubmitField('Add Session')


# class ActiveForm(FlaskForm):
#   sessions = db.get_sessions()
#   descriptions = db.get_descriptions()
#  choiceList = []
# for i in range(len(sessions)):
#        choiceList.append((sessions[i], descriptions[i]))
#
#   change_active = RadioField("Make Active", choices=choiceList, coerce=int)
#  Submit = SubmitField('Change Activity')

@app.route('/manage-sessions/', methods=['GET', 'POST'])
def manage_sessions():
    add_session_form = NewSessionForm()

    if add_session_form.validate_on_submit():
        rowcount = db.add_session(add_session_form.description.data,
                                  add_session_form.active.data)
        if rowcount == 1:
            flash('New Session Added Successfully')
            return redirect(url_for('index'))
        else:
            flash('Transaction Failed')

    change_active_form = ActiveForm()

    if change_active_form.validate_on_submit():
        pass

    return render_template('manage_sessions.html', form1=add_session_form, form2=change_active_form)


if __name__ == '__main__':
    app.run()
