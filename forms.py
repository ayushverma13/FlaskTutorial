# to create your own signup form to use with flask
import flask_wtf
from flask_wtf import Flaskform
from wtforms import Stringfield, Passwordfield , Submitfield

class SignUpForm(Flaskform):
    username = Stringfield('Username')
    password = Passwordfield('Password')
    submit = Submitfield('Sign Up')
