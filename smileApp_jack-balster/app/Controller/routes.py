from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title="Smile Portal", posts=posts.all())


@bp_routes.route('/postsmile', methods=['GET', 'POST'])
def post_smile():
    form = PostForm()

    if form.validate_on_submit():
        # Create a new Post item based on the form input
        post = Post(title=form.title.data, body=form.body.data, happiness_level=form.happiness_level.data)

        # Iterate over selected tags and append them to Post.tags
        for selected_tag in form.tag.data:
            post.tags.append(selected_tag)
        
        # Insert the new post into the database
        db.session.add(post)
        db.session.commit()

        # Flash a success message
        flash(f'New smile post "{form.title.data}" created!', 'success')

        # Redirect to the index page
        return redirect(url_for('routes.index'))

    return render_template('create.html', title="Post New Smile", form=form)


@bp_routes.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    # Retrieve the post with id post_id from the database
    post = Post.query.get(post_id)

    if post:
        # Increment the post's like count by 1
        post.likes += 1

        # Write the updated post back to the database
        db.session.commit()

        # Redirect to routes.index to reload the main page with the updated post
        return redirect(url_for('routes.index'))

    # Handle the case where the post with the given ID is not found
    flash(f'Post with ID {post_id} not found.', 'danger')
    return redirect(url_for('routes.index'))
