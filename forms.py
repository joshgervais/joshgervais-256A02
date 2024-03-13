from wtforms import Form, SelectField, IntegerField, FloatField, SubmitField, StringField, DateField
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = RadioField('Role', choices=[('c', 'Customer'), ('s', 'Staff')], validators=[DataRequired()])
    submit = SubmitField('Register')

class OrderForm(FlaskForm):
    type = SelectField('Type', choices=[], validators=[DataRequired()])
    crust = SelectField('Crust', choices=[], validators=[DataRequired()])
    size = SelectField('Size', choices=[], validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=10)])
    price_per = FloatField('Price Per Pizza', validators=[DataRequired()])
    order_date = DateField('Order Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Place Order')
