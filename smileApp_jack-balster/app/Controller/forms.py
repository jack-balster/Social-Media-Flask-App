from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import  DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from app.Model.models import Post, Tag

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
