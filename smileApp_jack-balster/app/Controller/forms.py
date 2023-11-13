from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import  DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.Model.models import Post, Tag, User

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    body = TextAreaField('Smile Message', validators=[
        DataRequired(message='Smile message is required.'),
        Length(max=1500, message='Smile message cannot exceed 1500 characters.')
    ])
    tag = QuerySelectMultipleField(
        'Tag',
        query_factory=lambda: Tag.query.all(),  # Query to fetch all tags from the Tag table
        get_label=lambda tag: tag.name,  # Use the 'name' attribute of the Tag object as the label
        widget=ListWidget(prefix_label=False),
        option_widget=CheckboxInput()
    )
    submit = SubmitField('Post')


class SortForm(FlaskForm):
    sort_by = SelectField(
        'Sort By',
        choices=[(1, 'Title'),       # Use integer values for sorting options
            (2, '# of Likes'),  # Use integers, not strings
            (3, 'Happiness Level'),
            (4, 'Date'),],
        validators=[DataRequired()],
        default='date'
    )
    
    # Add a BooleanField checkbox for displaying user posts
    display_my_posts_only = BooleanField('Display my posts only')
    
    refresh = SubmitField('Refresh')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
