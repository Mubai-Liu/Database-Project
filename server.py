
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
import re
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, session

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = '4111'

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.243.220.243/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.243.220.243/proj1part2"
#
DATABASEURI = "postgresql://ml4407:5974@35.231.103.173/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute("""CREATE TABLE IF NOT EXISTS test (
#   id serial,
#   name text
# );""")

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



#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  return render_template('index.html')
# def index():
#   """
#   request is a special object that Flask provides to access web request information:

#   request.method:   "GET" or "POST"
#   request.form:     if the browser submitted a form, this contains the data in the form
#   request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

#   See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
#   """

#   # DEBUG: this is debugging code to see what request looks like
#   print(request.args)


#   #
#   # example of a database query
#   #
#   cursor = g.conn.execute("SELECT username FROM person;")
#   names = []
#   for result in cursor:
#     names.append(result[0])  # can also be accessed using result[0]
#   cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #  context = dict(data = names)

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  #return render_template("index.html", **context)

@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = g.conn.execute('SELECT person_id, username FROM person WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            #session['id'] = account['person_id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/pythonlogin/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# @app.route('/home')
# def home():
#   return redirect('/')



#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/pythonlogin/another')
def another():
  return render_template("register.html")

# @app.route('/companyInfo')
# def companyListing():
#     cursor = g.conn.execute("SELECT  FROM Company")
#     return render_template("index.html", **context)



@app.route('/pythonlogin/companyListing', methods = ['GET'])
def companyListing():
  cursor = g.conn.execute(
    "SELECT C.Company_Name, I.Industry FROM Company C JOIN C_Industry I ON C.Company_id = I.Company_id")
  names = []
  names.append(["Company Name", "Industry"])
  for result in cursor:
    names.append(result)
  cursor.close()
  context = dict(data = names)
  return render_template("home.html", **context)


@app.route('/pythonlogin/jobListing', methods = ['GET'])
def jobListing():
  cursor = g.conn.execute(
    "SELECT Title, Company_Name FROM Job")
  names = []
  names.append(["Job Title", "Company Name"])
  for result in cursor:
    names.append(result)
  cursor.close()
  context = dict(data = names)
  return render_template("home.html", **context)


@app.route('/pythonlogin/companyInfo', methods=['POST'])
def companyInfo():
  name = request.form['name']
  name = name + '%'
  if (name != ''):
    cursor =  g.conn.execute("SELECT C.Company_Name, City, State, Description, Company_Size, Average_Salary,Username, Comment,Rating FROM Company C LEFT OUTER JOIN ( SELECT Company_ID, Username, Comment, Rating FROM Has_CR JOIN CompanyReview CR ON Has_CR.CR_ID = CR.CR_ID) R ON C.Company_ID = R.Company_ID WHERE lower(C.Company_Name) LIKE lower((%s))",  name) 
    names = []
    names.append(["Company Name", "City", "State","Company Description","Company Size", "Average Salary", "Username", "Comment","Rating"])
    for result in cursor:
      names.append(result)
    cursor.close()
    context = dict(data = names)
  else:
    names = []
    context = dict(data = names)
  return render_template("home.html", **context)

@app.route('/pythonlogin/addCR', methods=['POST'])
def addCR():
  if 'username' in request.form and 'companyName' in request.form and'comment' in request.form and 'rating' in request.form:
      username = request.form['username']
      companyName = request.form['companyName']
      comment = request.form['comment']
      rating = request.form['rating']
      g.conn.execute('INSERT INTO CompanyReview(Username,Comment,Rating) VALUES (%s, %s, %s)', (username, comment, rating)) 
      g.conn.execute('INSERT INTO has_CR(Company_ID, CR_ID) VALUES (SELECT Company_ID FROM Company WHERE lower(company_name) LIKE lower((%s)), SELECT CR_ID FROM CompanyReview WHERE comment = %s)',(companyName,comment))
  return render_template("index.html", **context)


@app.route('/pythonlogin/jobInfo', methods=['POST'])
def jobInfo():
  name = request.form['name']
  name = name + '%'
  if (name != '%'):
    cursor =  g.conn.execute("SELECT sub1.title, sub1.Company_Name, Description, Username, Job_Start_time, Rating, Comment, Interview_Date, Difficulty_level, Question FROM (SELECT J.Title, J.Company_Name, Description, Username, Job_Start_time, Rating, Comment FROM Job J LEFT OUTER JOIN (SELECT Title, Company_Name, Username,Job_Start_time, Rating, Comment FROM Has_JR JOIN JobReview JR ON Has_JR.JR_ID = JR.JR_ID) JR ON J.title = JR.title AND J.Company_Name=JR.Company_Name) sub1 FULL JOIN (SELECT J.Title, J.Company_Name, Interview_Date, Difficulty_level, Question FROM Job J LEFT OUTER JOIN (SELECT Title, Company_Name,  Interview_Date, Difficulty_level, Question FROM Has_IR JOIN (SELECT IR.IR_ID, username, Interview_Date, Difficulty_level, Question FROM interviewReview IR LEFT OUTER JOIN ir_question Q ON IR.IR_ID=Q.IR_ID) IR ON has_IR.IR_ID=IR.IR_ID) IR ON J.title = IR.title AND J.Company_Name=IR.Company_Name) sub2 ON sub1.title=sub2.title AND sub1.Company_Name=sub2.Company_Name WHERE LOWER(sub1.title) LIKE LOWER((%s));", name) 
    names = []
    names.append(["Job Title", "Company Name", "Job Description","User Name","Start Time of the Job","Job Rating"," Job Comment","Interview Date","Difficulty Level","Question Asked"])
    for result in cursor:
      names.append(result)
    cursor.close()
    context = dict(data = names)
  else:
    names = []
    context = dict(data = names)
  return render_template("home.html", **context)

@app.route('/addJR', methods=['POST'])
def addJR():
  if 'username' in request.form and 'companyName' in request.form and'comment' in request.form and 'rating' in request.form:
      username = request.form['username']
      companyName = request.form['companyName']
      comment = request.form['comment']
      rating = request.form['rating']
      g.conn.execute('INSERT INTO CompanyReview(Username, Company_ID, Comment,Rating) VALUES (%s, SELECT Company_ID FROM Company WHERE lower(Company_Name) LIKE lower((%s)), %s, %s)', (username, companyName, comment, rating))
  return render_template("index.html", **context)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) ', name)
  return redirect('/')


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        degree = request.form['degree']
        cursor = g.conn.execute("SELECT * FROM person WHERE username = %s", (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            g.conn.execute('INSERT INTO person(username, password, email, city, state, degree) VALUES (%s, %s, %s, %s, %s, %s)', (username, password, email,
            city, state, degree))
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/pythonlogin/showperson', methods = ['GET'])
def showperson():
  cursor = g.conn.execute(
    "SELECT * FROM Person")
  names = []
  names.append(["id", "username"])
  for result in cursor:
    names.append(result)
  cursor.close()
  context = dict(data = names)
  return render_template("home.html", **context)




# @app.route('/login')
# def login():
#     abort(401)
#     this_is_never_executed()

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
