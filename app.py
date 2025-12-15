from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)


import os
# Use the Vercel temporary directory (or a standard writable path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    Sno=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self)->str: #->str means the function returns a string
        return f"{self.Sno} - {self.title}  "
    
# Add this block:
with app.app_context():
    db.create_all()


@app.route("/",methods=['GET','POST'])
def hello_world():
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo=Todo.query.all()
    print(allTodo)
    
    return render_template("index.html",allTodo=allTodo)
#return 'Hello, World!'

# @app.route("/products")
# def products():
#     return "<p>pRODUCT</p>"

@app.route("/show")
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return "this is products page"

@app.route("/update/<int:Sno>",methods=['GET','POST'])
def update(Sno):
    if request.method=="POST":
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(Sno=Sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(Sno=Sno).first()
    return render_template("update.html",todo=todo)


@app.route("/delete/<int:Sno>")
def delete(Sno):
    allTodo=Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(allTodo)
    db.session.commit()
    print(allTodo)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)