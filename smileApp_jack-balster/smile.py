from app import create_app, db
from app.Model.models import Post, Tag, postTags

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'Post': Post, 'User': User}

@app.before_request
def initDB(*args, **kwargs):
    if app.got_first_request:
        db.create_all()
        if Tag.query.count() == 0:
             tags = ['funny','inspiring', 'true-story', 'heartwarming', 'friendship']
             for t in tags:
                 db.session.add(Tag(name=t))
             db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)