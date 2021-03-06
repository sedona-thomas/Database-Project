
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

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# postgresql://USER:PASSWORD@34.73.36.248/project1
DATABASEURI = "postgresql://jjk2235:512791@34.73.36.248/project1"
engine = create_engine(DATABASEURI)

'''
    Main
'''

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
  global CURRENT_USER_ID
  CURRENT_USER_ID = int(user_ids[0])
  return redirect('/')

'''
    Home
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
  
  '''
  # delete if this section doesnt mess up the server
  print(request.args)

  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
  '''
  
  if CURRENT_USER_ID == None:
    username = None
  else:
    cursor = g.conn.execute("SELECT name FROM users WHERE user_id = %s", CURRENT_USER_ID)
    username = []
    for result in cursor:
      username.append(result['name'])  # can also be accessed using result[0]
    cursor.close()
    username = username[0]
  context = {"CURRENT_USER_ID": CURRENT_USER_ID, "username": username}
  
  # delete if above section is deleted
  #context["data"] = names

  return render_template("index.html", **context)

# localhost:8111/index.html
# equivalent to localhost:8111/
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

# localhost:8111/package_containment
@app.route('/package_containment', methods=["POST"])
def package_containment():
  command = text("SELECT DISTINCT module.* FROM module, package_module_containment pmc WHERE module.name = pmc.module_name AND pmc.package_name = '{0}'".format(request.form['package_name']));
  cursor = g.conn.execute(command)
  data = []
  for result in cursor:
    data.append(result)
  cursor.close()
  context = dict(data = data, title = request.form['package_name'])
  return render_template("search_results.html", **context)

# localhost:8111/module_containment
@app.route('/module_containment', methods=["POST"])
def module_containment():
  command1 = text("SELECT DISTINCT method.* FROM method, module_method_containment mmc WHERE method.name = mmc.method_name AND mmc.module_name = '{0}'".format(request.form['module_name']))
  cursor1 = g.conn.execute(command1)
  method_data = []
  for result in cursor1:
    method_data.append(result)
  cursor1.close()
  command2 = text("SELECT DISTINCT constant.* FROM constant, module_constant_containment mcc WHERE constant.name = mcc.constant_name AND mcc.module_name = '{0}'".format(request.form['module_name']))
  cursor2 = g.conn.execute(command2)
  constant_data = []
  for result in cursor2:
    constant_data.append(result)
  cursor2.close()
  command3 = text("SELECT DISTINCT imported_module_name FROM module_dependencies WHERE module_dependencies.module_name = '{0}'".format(request.form['module_name']))
  cursor3 = g.conn.execute(command3)
  dependency_data = []
  for result in cursor3:
    dependency_data.append(result)
  cursor3.close()
  title1 = "Methods contained within {0}".format(request.form['module_name'])
  title2 = "Constants contained within {0}".format(request.form['module_name'])
  context = dict(method_data = method_data, constant_data = constant_data, dependency_data = dependency_data, title1 = title1, title2 = title2)
  return render_template("module_results.html", **context)


# localhost:8111/about_you
# "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'method' ORDER BY ORDINAL_POSITION"
@app.route('/about_you')
def about_you():
  if CURRENT_USER_ID == None:
    return "You are not logged in. Please return to the homepage and add yourself as a user or log in."
  command1 = text("SELECT DISTINCT method.* FROM method, method_keywords, method_favorite WHERE ((method_keywords.name = method.name) AND (method.name = method_favorite.method_name) AND (user_id = {0}))".format(CURRENT_USER_ID))
  cursor1 = g.conn.execute(command1)
  command2 = text("SELECT DISTINCT constant.* FROM constant, constant_keywords, constant_favorite WHERE ((constant_keywords.name = constant.name) AND (constant.name = constant_favorite.constant_name) AND (user_id = {0}))".format(CURRENT_USER_ID))
  cursor2 = g.conn.execute(command2)
  command4 = text("SELECT DISTINCT module.* FROM module, module_keywords, module_favorite WHERE ((module_keywords.name = module.name) AND (module.name = module_favorite.module_name) AND (user_id = {0}))".format(CURRENT_USER_ID))
  cursor4 = g.conn.execute(command4)
  command5 = text("SELECT * FROM user_code NATURAL JOIN code WHERE (user_id = {0})".format(CURRENT_USER_ID))
  cursor5 = g.conn.execute(command5)
  command6 = text("SELECT name FROM users WHERE user_id = {0}".format(CURRENT_USER_ID))
  cursor6 = g.conn.execute(command6)
  method_data = []
  constant_data = []
  module_data = []
  user_code = []
  usernames = []
  for result in cursor1:
    method_data.append(result)
  for result in cursor2:
    constant_data.append(result)
  for result in cursor4:
    module_data.append(result)
  for result in cursor5:
    user_code.append(result)
  cursor1.close()
  for result in cursor6:
    usernames.append(result)
  cursor6.close()
  cursor2.close()
  cursor4.close()
  cursor5.close()
  username = usernames[0][0]
  context = dict(username = username, method_data=method_data, constant_data=constant_data, module_data=module_data, user_code=user_code)
  return render_template("about_you.html", **context)

# localhost:8111/contributors
@app.route('/contributors')
def contributors():
  cursor = g.conn.execute("SELECT DISTINCT users.name FROM users WHERE users.user_id IN (SELECT contributor.user_id FROM contributor)")
  data = []
  for result in cursor:
    data.append(result)
  cursor.close()
  context = dict(data = data)
  return render_template("contributors.html", **context)

'''
    Searches
'''

# currently gives filepath for given package or module
@app.route('/search_results', methods=['POST'])
def search_results():
  cursor = g.conn.execute("SELECT github_link FROM code WHERE filepath in (SELECT package.filepath FROM package WHERE package.name LIKE %s) OR filepath in (SELECT module.filepath FROM module WHERE module.name LIKE %s)",request.form['code'],request.form['code'])
  data = []
  for result in cursor:
    data.append(str(result[0]))
  cursor.close()
  context = dict(data = data)
  context["title"] = "Github link(s) for {}".format(request.form['code'])
  return render_template("github_results.html", **context)

# looks up by keyword and selected type of thing
@app.route('/keyword_results',methods=['POST'])
def keyword_results():
  command = text("SELECT {1}.* FROM {1}, {1}_keywords WHERE ('{0}' = {1}_keywords.keyword) AND ({1}_keywords.name = {1}.name)".format(request.form['keyword'], request.form['type_name']))
  cursor = g.conn.execute(command)
  data = []
  for result in cursor:
    data.append(result)
  cursor.close()
  context = dict(data = data)
  context["title"] = "Searched {} from {}".format(request.form['keyword'], request.form['type_name'])
  return render_template("keyword_results.html", **context)

# looks up by related keywords and selected type of thing
@app.route('/related_keyword_search',methods=['POST'])
def related_keyword_search():
  # SELECT similar_keywords.keyword1 FROM similar_keywords WHERE similar_keywords.keyword1 = 'e' OR similar_keywords.keyword2 = 'e' UNION SELECT similar_keywords.keyword2 FROM similar_keywords WHERE similar_keywords.keyword1 = 'e' OR similar_keywords.keyword2 = 'e';
  # SELECT similar_keywords.keyword1 FROM similar_keywords WHERE similar_keywords.keyword1 = {0} OR similar_keywords.keyword2 = {0} UNION SELECT similar_keywords.keyword2 FROM similar_keywords WHERE similar_keywords.keyword1 = {0} OR similar_keywords.keyword2 = {0}
  command = text("SELECT DISTINCT {1}.* FROM {1}, {1}_keywords WHERE ({1}_keywords.keyword in (SELECT similar_keywords.keyword1 FROM similar_keywords WHERE similar_keywords.keyword1 = '{0}' OR similar_keywords.keyword2 = '{0}' UNION SELECT similar_keywords.keyword2 FROM similar_keywords WHERE similar_keywords.keyword1 = '{0}' OR similar_keywords.keyword2 = '{0}') AND ({1}_keywords.name = {1}.name))".format(request.form['keyword'], request.form['type_name']))
  cursor = g.conn.execute(command)
  data = []
  for result in cursor:
    data.append(result)
  cursor.close()
  context = dict(data = data)
  context["title"] = "Searched related to {} from {}".format(request.form['keyword'], request.form['type_name'])
  return render_template("keyword_results.html", **context)

# looks up by keyword and selected type of thing in favorites
@app.route('/favorite_results',methods=['POST'])
def favorite_results():
  #command below worked as intended
  #SELECT method.* FROM method, method_keywords, method_favorite WHERE ('equal' = method_keywords.keyword) AND (method_keywords.name = method.name) AND (method.name = method_favorite.method_name) AND (user_id = 1)
  command = text("SELECT {2}.* FROM {2}, {2}_keywords, {2}_favorite WHERE ('{1}' = {2}_keywords.keyword) AND ({2}_keywords.name = {2}.name) AND ({2}.name = {2}_favorite.{2}_name) AND (user_id = {0})".format(CURRENT_USER_ID, request.form['keyword'], request.form['type_name']))
  cursor = g.conn.execute(command)
  data = []
  for result in cursor:
    data.append(result)
  cursor.close()
  context = dict(data = data)	
  context["title"] = "Searched favorites for {} from {}".format(request.form['keyword'], request.form['type_name'])
  return render_template("keyword_results.html", **context)

'''
    Add Information to Database
'''

# add user to database
@app.route('/add_user', methods=['POST'])
def add_user():
  cursor = g.conn.execute("SELECT MAX(user_id) as max FROM users")
  user_ids = []
  for result in cursor:
    user_ids.append(result['max'])
  cursor.close()
  user_id = int(user_ids[0]) + 1
  name = request.form['name']
  g.conn.execute('INSERT INTO users(user_id, name) VALUES (%s, %s)', user_id, name)
  return redirect('/')

# add favorites to database
@app.route('/add_favorite', methods=['POST'])
def add_favorite():
  #below command worked as intended
  #INSERT INTO module_favorite(user_id, module_name) VALUES (1, 'numpy')
  command = text("INSERT INTO {0}_favorite(user_id,{0}_name) VALUES({1},'{2}')".format(request.form['type_name'], CURRENT_USER_ID, request.form['name']))
  g.conn.execute(command)
  return redirect('/')

# add user code to database
@app.route('/add_user_code', methods=['POST'])
def add_user_code():
  
  cursor = g.conn.execute("SELECT * FROM contributor where contributor.user_id = %s", CURRENT_USER_ID)
  user_ids = []
  for result in cursor:
    user_ids.append(result['user_id'])
  cursor.close() 
  if CURRENT_USER_ID not in user_ids:
    cursor = g.conn.execute("SELECT MAX(author_id) as max FROM author")
    author_ids = []
    for result in cursor:
      author_ids.append(result['max'])
    cursor.close()
    author_id = int(author_ids[0]) + 1
    g.conn.execute('INSERT INTO author(author_id,name) VALUES (%s, %s)', author_id, CURRENT_USER_ID)
    g.conn.execute('INSERT INTO contributor(author_id,user_id) VALUES (%s, %s)', author_id, CURRENT_USER_ID)
  g.conn.execute('INSERT INTO code(filepath, filename, github_link) VALUES (%s, %s, %s)', request.form['filepath'], request.form['filename'], request.form['github_link'])
  g.conn.execute('INSERT INTO user_code(filepath, user_id) VALUES (%s, %s)', request.form['filepath'], CURRENT_USER_ID)
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
