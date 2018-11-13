from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://build-a-blog:blogbuilder@localhost:3306/build-a-blog"
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

class Posts(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))


    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/", methods=["POST","GET"])

def index():
    if request.method == 'POST':
        title_name = request.form['title']
        body_name = request.form['body']
        new_post = Posts(title_name,body_name)
        db.session.add(new_post)
        db.session.commit()

    posts = Posts.query.all()
    return render_template('index.html',title="main page", posts=posts)



if __name__ == "__main__":
    app.run()