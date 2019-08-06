import os

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# set the db folder and name relative to the application root folder
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{os.path.join(project_dir,'bookdatabase.db')}"
print(f"database located at:{database_file}")

app = Flask(__name__)

# bind the app and the db location
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

# initialize the connction to the database and keep this in db variable
db=SQLAlchemy(app)


# class Book, will create a table in db

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    
    # default representer for the Book class. This will allow to use 'print(book)' and 
    # receive a meaningful output.
    def __repr__(self):
        return "<Title: {}".format(self.title)


# to initiate the database use the foolowing
# >python
# >>>from app import db
# >>>db.create_all()
# >>>exit()


# main route of the applicaiton
# by default, flask accepts GET request for all routes
# adding 'methods=["GET", "POST"]' to the route decorator will solve 'Method not allowed'
# error after submitting the form
@app.route("/", methods=["GET", "POST"]) 
def home():
    if request.form:
        try:
            book = Book(title=request.form.get("title"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)

    books = Book.query.all()
    return render_template("index.html", books=books)

@app.route("/update", methods=["POST"])
def update():
    try:
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")
        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle
        db.session.commit()
    except Exception as e:
        print("Failed to update book title")
        print(e)
    return redirect("/")    


@app.route("/delete", methods=["POST"])
def delete():
    try:
        title = request.form.get("title")
        book = Book.query.filter_by(title=title).first()
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        print("Failed to delete book")
        print(e)
    
    return redirect("/")    

if __name__ == "__main__":
    app.run()