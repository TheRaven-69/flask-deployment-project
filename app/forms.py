from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, URL, Optional


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 128)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class ProfileForm(FlaskForm):
    full_name = StringField('Full name', validators=[Length(0, 120)])
    bio = TextAreaField('Bio', validators=[Length(0, 500)])
    avatar = FileField('Avatar')
    submit = SubmitField('Save')

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(3, 200)])
    summary = TextAreaField('Короткий опис', validators=[DataRequired(), Length(3, 500)])
    content = TextAreaField('Текст', validators=[DataRequired()])
    image_url = StringField('URL зображення', validators=[URL(), Optional()])
    submit = SubmitField('Створити новину')
