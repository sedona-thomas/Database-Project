
"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import sql_methods # app specific methods in sql_methods.py

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# postgresql://USER:PASSWORD@34.73.36.248/project1
DATABASEURI = "postgresql://jjk2235:512791@34.73.36.248/project1"
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.
  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass



'''
    User Information
'''

CURRENT_USER_ID = None

# select a user from the database
@app.route('/choose_user', methods=['POST'])
def choose_user():
  
  username = request.form['username']
  cursor = g.conn.execute("SELECT user_id FROM users WHERE name = %s", username)
  user_ids = []
  for result in cursor:
    user_ids.append(result['user_id'])  # can also be accessed using result[0]
  cursor.close()

  CURRENT_USER_ID = int(user_ids[0])
  return redirect('/')



'''
    Navigation
'''

# localhost:8111/
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:
      request.method:   "GET" or "POST"
      request.form:     if the browser submitted a form, this contains the data in the form
      request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2
  See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
  """
  
  print(request.args)

  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)

  return render_template("index.html", **context, CURRENT_USER_ID)

# localhost:8111/index.html
@app.route('/index.html')
def other_index():
    return index()


'''
    Database Pages
'''

# localhost:8111/packages
@app.route('/packages')
def packages():
  cursor = g.conn.execute("SELECT * FROM package")
  data = []
  for result in cursor:
    data.append(result)
  cursor.close()
  context = dict(data = data)
  return render_template("packages.html", **context)

# localhost:8111/modules
@app.route('/modules')
def modules():
  cursor = g.conn.execute("SELECT * FROM module")
  data = []
  for result in cursor:
    data.append(result)
  cursor.close()
  context = dict(data = data)
  return render_template("modules.html", **context)

# localhost:8111/methods
@app.route('/methods')
def methods():
  cursor = g.conn.execute("SELECT * FROM method")
  data = []
  for result in cursor:
    data.append(result)
  cursor.close()
  context = dict(data = data)
  return render_template("methods.html", **context)

# localhost:8111/constants
@app.route('/constants')
def constants():
  cursor = g.conn.execute("SELECT * FROM constant")
  data = []
  for result in cursor:
    data.append(result)
  cursor.close()
  context = dict(data = data)
  return render_template("constants.html", **context)


'''
    Add Information to Database
'''

# add user to database
@app.route('/add_user', methods=['POST'])
def add_user():
    
  cursor = g.conn.execute("SELECT MAX(user_id) as max FROM users")
  user_ids = []
  for result in cursor:
    user_ids.append(result['max'])  # can also be accessed using result[0]
  cursor.close()
  
  user_id = int(user_ids[0]) + 1
  name = request.form['name']
  
  g.conn.execute('INSERT INTO users(user_id, name) VALUES (%s, %s)', user_id, name)
  return redirect('/')



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:
        python server.py
    Show the help text using:
        python server.py --help
    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

  run()




'''
    Miscellaneous
'''

# @app.route("/foobar/", methods=["POST", "GET"])
# see for routing: https://flask.palletsprojects.com/en/1.1.x/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/

'''
# localhost:8111/another_page
@app.route('/another_page')
def another_page():
  return render_template("another_page.html")
'''

'''
@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()
'''

'''
# execute SQL command in database
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
'''

'''
# localhost:8111/
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:
      request.method:   "GET" or "POST"
      request.form:     if the browser submitted a form, this contains the data in the form
      request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2
  See its API: https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data
  """
  
  print(request.args)

  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  context = dict(data = names)

  return render_template("index.html", **context)
'''
