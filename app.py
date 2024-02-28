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
    instruction = request.args.get('instruction')
    try:
        documents = CodeState.query.limit(100).all()
        # If there's no instruction from submission, try to read the last instruction from file
        if not instruction:
            try:
                with open('instructions.txt', 'r') as f:
                    instruction = f.readlines()[-1].strip()  # Read the last line as the latest instruction
            except FileNotFoundError:
                instruction = "No instruction submitted yet."
        return render_template('index.html', documents=documents, instruction=instruction)
    except Exception as e:
        return str(e)  # display the error on the web page

@app.route('/submit-instruction', methods=['POST'])
def submit_instruction():
    instruction_text = request.form['instruction']
    
    # Save the instruction in a text file
    with open('instructions.txt', 'a') as f:
        f.write(instruction_text + "\n")
    
    # Optionally, redirect to a new page or back to the home page
    return redirect(url_for('home', instruction=instruction_text))



if __name__ == '__main__':
    with app.app_context():
        # Check if there's data in the CodeState table
        if not CodeState.query.first():
            print("No data found in the database.")
        
         
        
    app.run(debug=True)
