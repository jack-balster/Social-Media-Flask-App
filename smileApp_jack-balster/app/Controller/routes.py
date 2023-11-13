from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from app import db
from app.Model.models import Post, Tag, postTags
from app.Controller.forms import PostForm, SortForm
from flask_login import current_user, login_required

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET', 'POST'])  # Accept both GET and POST requests
@bp_routes.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    sortform = SortForm()
    
    if request.method == 'POST':
        # Retrieve the sorting choice from the form and convert it to an int
        sort_choice = int(sortform.sort_by.data)
        
        # Check if the "Display my posts only" checkbox is selected
        display_my_posts_only = sortform.display_my_posts_only.data
        
        if display_my_posts_only:
            # Filter and sort only the current user's posts
            user_posts = current_user.get_user_posts().order_by(Post.timestamp.desc())
            posts = user_posts
        else:
            # Sort all posts by the selected criteria
            if sort_choice == 1:  # Sort by Title
                posts = Post.query.order_by(Post.title)
            elif sort_choice == 2:  # Sort by Number of Likes
                posts = Post.query.order_by(Post.likes.desc())
            elif sort_choice == 3:  # Sort by Happiness Level
                posts = Post.query.order_by(Post.happiness_level.desc())
            else:  # Default: Sort by Date (most recent first)
                posts = Post.query.order_by(Post.timestamp.desc())
    else:
        # Default: Sort by Date (most recent first)
        posts = Post.query.order_by(Post.timestamp.desc())

    return render_template('index.html', title="Smile Portal", posts=posts.all(), sortform=sortform) 


@bp_routes.route('/postsmile', methods=['GET', 'POST'])
@login_required
def post_smile():
    form = PostForm()

    if form.validate_on_submit():
        # Create a new Post item based on the form input
        post = Post(title=form.title.data, 
                    body=form.body.data, 
                    happiness_level=form.happiness_level.data,
                    user_id=current_user.id)

        
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
@login_required
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


@bp_routes.route('/delete/<int:post_id>', methods=['DELETE', 'POST'])
@login_required
def delete_post(post_id):
    # Query the Post table to get the post with id=post_id
    post = Post.query.get(post_id)

    if post:

        for tag in post.tags:
            post.tags.remove(tag)

        db.session.commit()

        # Delete the post
        db.session.delete(post)
        db.session.commit()

        flash(f'Post "{post.title}" has been deleted.', 'success')
    else:
        flash(f'Post with ID {post_id} not found.', 'danger')

    # Redirect to routes.index
    return redirect(url_for('routes.index'))
