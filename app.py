from flask import Flask, render_template, request, redirect, url_for
import os, random
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy import MetaData

from pedal import Feedback
import subprocess
import tempfile
import os
import textwrap

from utils import is_json 
import re


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, 'cleansampledata.db')
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
    
    print("Instruction Text:")
    print(instruction_text)

    # student_code = """
    # def summate(values):
    #     total = 0
    #     for v in values:
    #         total += v
    #         print(total)
    #     return total

    # print(summate([1, 2, 3]))
    # """

    # Initialize the passed count
    passed_count = 0

    # Fetch the student submission from the CodeState table
    submissions = CodeState.query.all()

    # Loop through the submissions
    for submission in submissions:
        student_code = submission.contents

    # # retrieve the student submission from the database
    # submission = CodeState.query.order_by(func.random()).first()
    # student_code = submission.contents

        # check if the submission is JSON, skip if true
        if is_json(submission.contents):
            print("Skipping JSON content")
            
        else:
            # format the student code
            student_code = textwrap.dedent(student_code)
            print("Student Submission:")
            print(student_code)

            try:
            # Create temporary files for instructor script and student submission
                with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', prefix='instructor_', delete=False) as instructor_script_file:
                    instructor_script_file.write(instruction_text)
                    instructor_script_filepath = instructor_script_file.name

                with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', prefix='student_', delete=False) as student_submission_file:
                    student_submission_file.write(student_code)
                    student_submission_filepath = student_submission_file.name

                # Construct the Pedal CLI command
                pedal_command = f"pedal feedback {instructor_script_filepath} {student_submission_filepath}"

                # Run the Pedal command using subprocess
                result = subprocess.run(pedal_command, shell=True, capture_output=True, text=True)

                # Get the output and return it as a JSON response
                print("result:")
                print(result.stdout)


                # Extract the score from the output
                score_match = re.search(r"Score: (\d)", result.stdout)
                if score_match:
                    score = int(score_match.group(1))

                    # Increment the score count
                    if score == 1:
                        passed_count += 1

            # except Exception as e:
            #     # Handle errors, if any
            #     return jsonify({'result': 'error', 'error_message': str(e)})
            finally:
                # Cleanup: remove temporary files
                os.remove(instructor_script_filepath)
                os.remove(student_submission_filepath)

    print("Number of submission passed", passed_count)
    print("Total number of submission", len(submissions))

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
