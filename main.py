from flask import Flask, render_template, request, jsonify
from uuid import uuid4
import time

from list_solver import list_solver
from list_validator import list_validator


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)



threaded_processes = {}




app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/_validate')
def _validate():

    username = request.args.get('username', '', type=str)
    password = request.args.get('password', '', type=str)
    link = request.args.get('link', '', type=str)

    validator = list_validator(username, password, link)
    validator.start()

    # Dynamic wait for values to change from initial None
    while(validator.get_link_valid() == None or validator.get_creds_valid() == None):
        print("values not ready yet")
        time.sleep(0.5)

    link_valid = validator.get_link_valid()
    login_valid = validator.get_creds_valid()
    print("link valid: " + str(link_valid))
    print("login_valid: " + str(login_valid))

    print("validator alive?")
    print(validator.is_alive())

    return jsonify(loginValid = login_valid, linkValid = link_valid)


@app.route('/_start_process')
def _start_process():
    
    list_link = request.args.get('list_link', '', type=str)
    email = request.args.get('email', '', type=str)
    username = request.args.get('username', '', type=str)
    password = request.args.get('password', '', type=str)
    
    # create new solver object
    solver = list_solver(list_link, username, password, email)
    # start, then look for validity. If not valid, kill.
    solver.start()
    # add object to threaded_processes dictionary
    key = str(uuid4())
    threaded_processes[key] = solver
    print("threaded processes from start_process")
    print(threaded_processes)

    percent_done = threaded_processes[key].percent_done()
    completed_words = threaded_processes[key].get_completed_words()
    current_word = threaded_processes[key].get_current_word()
    correct_definition = threaded_processes[key].get_correct_definition()
    current_operation = threaded_processes[key].get_current_operation()
    current_command = threaded_processes[key].get_command_output()
    ellapsed_time = threaded_processes[key].get_time_ellapsed()

    #loginValid = threaded_processes[key].get_creds_valid()

    return jsonify(
        percent = percent_done,
        words = completed_words,
        word = current_word,
        definition = correct_definition,
        operation = current_operation,
        command = current_command,
        time = ellapsed_time,
        key = key
    )


# jquery .get method calls _process_progress @route
@app.route('/_process_progress')
def _process_progress():
    

    # request.args.get used to get "dictionary" value from 'key': key
    key = request.args.get('key', '', type=str)
    if not key in threaded_processes:
        print(" ")
        print("key not found in list")
        print("key: " + str(key))
        print(" ")
        print(threaded_processes)
        print(" ")
    

    percent_done = threaded_processes[key].percent_done()
    completed_words = threaded_processes[key].get_completed_words()
    current_word = threaded_processes[key].get_current_word()
    correct_definition = threaded_processes[key].get_correct_definition()
    current_operation = threaded_processes[key].get_current_operation()
    current_command = threaded_processes[key].get_command_output()
    ellapsed_time = threaded_processes[key].get_time_ellapsed()
    
    
    done = False
    if percent_done == 100:
        done = True
        # debugging
        print(threaded_processes[key].is_alive())
        del threaded_processes[key]
    
    # _process_progress returns percent done to jquery .get function(data) as "data"
    # this data is then used in the progressbar
    return jsonify(
        percent = percent_done,
        words = completed_words,
        word = current_word,
        definition = correct_definition,
        operation = current_operation,
        command = current_command,
        time = ellapsed_time,
        done = done,
        key = key
    )
    # a uuid4 key must be generated uniquely so that each user can recieve the percent
    # of their individual instance/thread

    # return str(threaded_processes[thread_number].percent_done())

# Used for local development
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)

# MAKE APP ROUTE FOR CURRENT WORD, DEFINITION, FEED, ETC.