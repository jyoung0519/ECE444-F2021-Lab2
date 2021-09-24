from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required, Email
from flask import session, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

moment = Moment(app)
bootstrap = Bootstrap(app)

@app.route('/')
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')  
        old_email = session.get('email')

        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your UofT email!')

        if form.email.data is not None:
            session['email_text'] = 'Your UofT email is: ' + form.email.data
        if '@mail.utoronto.ca' not in form.email.data:
            session['email_text'] = 'Please use your UofT email'
        
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form = form, name = session.get('name'),
                           email = session.get('email'), email_text = session.get('email_text'))


    

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time = datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500

class NameForm(Form):
    name = StringField('What is your name?', validators =[Required()])
    email = StringField('What is your UofT email?', validators =[Required(), Email()])
    

    submit = SubmitField('Submit')

if __name__ == '__main__':
    app.run(debug=True)
