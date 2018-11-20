from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://build-a-blog:blogbuilder@localhost:3306/build-a-blog"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

class Entries(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))


    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/')
def index():
    return redirect('/blog')

@app.route('/blog')
def blog():
    blog_id = request.args.get('id')

    if blog_id == None:
        posts = Entries.query.all()
        return render_template('index.html', posts=posts, title='Build-a-blog')
    else:
        post = Entries.query.get(blog_id)
        return render_template('single_post.html', post=post, title='Single Post')

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['post_title']
        body = request.form['post_body']
        title_error = ''
        body_error = ''

        if not title:
            title_error = "Please make sure to type in a title to your post!"
        if not body:
            body_error = "Please make sure to add some content to the body of your post!"

        if not body_error and not title_error:
            new_post = Entries(title, body)     
            db.session.add(new_post)
            db.session.commit()        
            return redirect('/blog?id={}'.format(new_post.id)) 
        else:
            return render_template('single_post.html', title='New Post', title_error=title_error, body_error=body_error, 
                post_title=title, post_body=body)
    
    return render_template('form.html', title='New Post')

if  __name__ == "__main__":
    app.run()