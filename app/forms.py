from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import Login
from app import open_connection

class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Update')

    def validate_username(self, username):
        conn = open_connection()
        results = conn.execute("Select username from users;").fetchall()
        conn.close()
        alr_defined = False
        
        for val in results:
            if username.data == val[1]:
                alr_defined = True
        
        if alr_defined:
            raise ValidationError("Username Already Exists")
                


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    
class SearchForm(FlaskForm):
    loc_name = StringField('Location Name', validators=[DataRequired(), Length(min=2, max=20)])
    search = SubmitField('Search')
