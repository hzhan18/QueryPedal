from flask import Flask, render_template, request, send_file
import os, re, time, csv
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy import MetaData

from pedal import Feedback
import subprocess
import tempfile
import textwrap

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(basedir, '20testentries.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the data model to match the existing 'CodeState' table structure
class CodeState(db.Model):
    __tablename__ = 'CodeState'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    contenttype = db.Column(db.String(50), nullable=False)

# Track if an instruction has been submitted
instruction_submitted = False

@app.route('/')
def home():
    global instruction_submitted
    # Reset the instruction submitted variable
    instruction_submitted = False
    instruction = request.args.get('instruction', "from pedal import *")
    passed_count = request.args.get('passed_count')
    total_submissions = request.args.get('total_submissions')
    processing_time = request.args.get('processing_time')
    try:
        documents = CodeState.query.limit(100).all()
        # If there's no instruction from submission, try to read the last instruction from file
        if not instruction:
            try:
                with open('instructions.txt', 'r') as f:
                    instruction = f.readlines()[-1].strip()  # Read the last line as the latest instruction
            except FileNotFoundError:
                instruction = "No instruction submitted yet."
        return render_template('index.html', documents=documents, instruction=instruction, 
                               passed_count=passed_count, total_submissions=total_submissions, 
                               processing_time=processing_time, instruction_submitted=instruction_submitted)
    except Exception as e:
        return str(e)  # display the error on the web page

@app.route('/submit-instruction', methods=['POST'])
def submit_instruction():
    global instruction_submitted
    instruction_text = request.form['instruction']

    # Start the timer
    start_time = time.time()
    
    try:
        # Check instructor script syntax
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', prefix='instructor_', delete=False) as instructor_script_file:
            instructor_script_file.write(instruction_text)
            instructor_script_filepath = instructor_script_file.name
        
        # Check syntax using compile()
        with open(instructor_script_filepath, 'r') as f:
            compile(f.read(), instructor_script_filepath, 'exec')

    except SyntaxError as e:
        # Handle syntax errors in the instructor script
        return render_template('index.html', error_message=f"Syntax Error in Instructor Script: {e}")
    except Exception as e:
        # Handle other exceptions
        return render_template('index.html', error_message=f"Error occurred: {e}")
    finally:
        # Cleanup: remove temporary file
        os.remove(instructor_script_filepath)


    # Initialize the counters
    code_count = 0
    passed_count = 0
    invalid_count = 0
    failed_count = 0


    # Fetch the student submission from the CodeState table
    submissions = CodeState.query.all()
    ### Limit the number of submissions to 200 for testing
    # submissions = CodeState.query.limit(200).all()
    ### Fetch the last 200 submissions for testing
    # submissions = CodeState.query.order_by(CodeState.id.desc()).limit(200).all()[::-1]

    # Define total submissions
    total_submissions = len(submissions)

    # Loop through the submissions
    for submission in submissions:
        # Determine the content type and increment the counter
        if submission.contenttype == "code":
            code_count += 1
            # Get the student code from the submission
            student_code = submission.contents
            # format the student code
            student_code = textwrap.dedent(student_code)

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
                print(code_count)


                # Extract the score from the output
                score_match = re.search(r"Score: (\d)", result.stdout)
                if score_match:
                    score = int(score_match.group(1))

                    # Increment the score count
                    if score == 1:
                        passed_count += 1
                    else:
                        # Extract the feedback from the output
                        label_match = re.search(r"Label: (.+)", result.stdout)
                        if label_match:
                            label = label_match.group(1)
                            if label in ('indentation_error', 'syntax_error', 'initialization_problem', 'type_error','name_error', 'unexpected_error', 
                                         'value_error', 'unused_variable', 'unused_function', 'unused_parameter', 'unused_import', 'unused_class', 'unused_method'):
                                invalid_count += 1
                            else:
                                failed_count += 1
                        

            except Exception as e:
                # Handle errors, if any
                print(f"Error occurred: {e}")
            finally:
                # Cleanup: remove temporary files
                os.remove(instructor_script_filepath)
                os.remove(student_submission_filepath)

        else:
            invalid_count += 1

    # Print the final counts at the end of the loop for the testing stage, not reflected in the web page
    print("Number of passed submission", passed_count)
    print("Number of code submission", code_count)
    print("Number of invalid submission", invalid_count)
    print("Number of failed submission", failed_count)
    print("Total number of submissions", len(submissions))

    with open('instructions.txt', 'a') as f:
        f.write(instruction_text + "\n")

    # Check if the counts match the total number of submissions
    if code_count != failed_count + passed_count + invalid_count:
        print("Counts do not match")
    elif code_count != total_submissions:
        print("Counts do not match")
    else:
        print("Counts match")
    
    # End the timer
    end_time = time.time()
    processing_time = end_time - start_time
    print("Time taken:", processing_time)

    # Get the current date
    current_date = time.strftime('%Y-%m-%d') # Format: YYYY-MM-DD

    # Summarize the results
    analyzed_results = {'Date': current_date,
                        'Total': total_submissions, 
                        'Passed': passed_count, 
                        'Invalid': invalid_count, 
                        'Failed': failed_count, 
                        'Processing Time': f"{processing_time: .2f} seconds"}
    
    # Save the results to a CSV file
    with open('analyzed_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Date','Total', 'Passed', 'Invalid', 'Failed', 'Processing Time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(analyzed_results)

    instruction_submitted = True
    return render_template('index.html', instruction=instruction_text, passed_count=passed_count, invalid_count=invalid_count, failed_count=failed_count,
                       total_submissions=total_submissions, processing_time=processing_time, instruction_submitted=instruction_submitted)

@app.route('/export-results', methods=['GET'])
def export_results():
    return send_file('analyzed_results.csv', as_attachment=True, download_name='analyzed_results.csv')

if __name__ == '__main__':
    with app.app_context():
        # Check if there's data in the CodeState table
        if not CodeState.query.first():
            print("No data found in the database.")
    app.run(debug=True)
    