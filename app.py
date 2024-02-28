from flask import Flask, render_template, request, redirect, url_for
import os, random
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy import MetaData

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'testdataset.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the data model to match the existing 'CodeState' table structure
class CodeState(db.Model):
    __tablename__ = 'CodeState'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    contents = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    try:
        documents = CodeState.query.limit(100).all()
        return render_template('index.html', documents=documents)
    except Exception as e:
        return str(e)  # display the error on the web page


if __name__ == '__main__':
    with app.app_context():
        # Check if there's data in the CodeState table
        if not CodeState.query.first():
            print("No data found in the database.")
        
         
        
    app.run(debug=True)
