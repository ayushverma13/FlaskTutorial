import flask
from flask import request, jsonify, render_template
import sqlite3
from forms import SignUpForm

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/books', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    published = query_parameters.get('published')
    author = query_parameters.get('author')

    query = "SELECT * FROM books WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if published:
        query += ' published=? AND'
        to_filter.append(published)
    if author:
        query += ' author=? AND'
        to_filter.append(author)
    if not (id or published or author):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

@app.route('/about')
def about():
    return 'The about page'


@app.route('/blog/<blog_id>')
def blogwithid(blog_id):
    return 'This is the blog corresponding to '+ str(blog_id)

'''@app.route('/blog/<string:blog_id>')
def blogwithid(blog_id):
    return 'This is the blog corresponding to '+ blog_id'''

#### Never Return sentences but HTML (hardcoded here)   

@app.route('/blog')
def blog():
    return '''
    <html>
    <head> Balle oye </head>
    <body>
        <h1> "Welcome to this blog </h1>
        <p> Hi guys this is he author of this blog </p>
    </body>
    </html>

    '''
#### Render HTML through templates(blueprints of html codes)
'''@app.route('/blogtempl')
def blogtempl():
    return render_template('blog.html')'''

#### Return HTML through templates (flask has this amazing tool called jinja, 
#### jinja2 is the template engine that comes bundled with the flsk framework, it allows us to input data,
#### and variables into our templates)
#### very quick example
'''inside of this I’m gonna go ahead and say blog dot HTML
author is equal to Bob so in this
scenario I'm passing in a variable into
the render template function creating a
value Bob and inside of the blog that
HTML wherever I want to render this
variable I'm gonna use double curly
brackets that is the Jinja syntax
I'm gonna say author so again author is
a variable that I'm passing in into the
brand new template function and it will
recognize that I'm using author over
here and passing that value so now if I
go ahead and save this and restart a
server and refresh I am Bob the author
of this block so that is the power of
ginger guys again the syntax for ginger
is these double curly braces and then
placing the variable name inside we're
gonna play a lot with this in future'''
#you can also use conditional statements in jinja , eg used is showing if sunny or rainy , many used cases 
# eg. to hide content if user not logged in etc 

@app.route('/blogtempl')
def blogtempl():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    return render_template('blog.html', author = 'Bob', sunny = True, books= all_books)

# web forms with flask
'''app.config['Secret_key']= 'salman ka bacha' 

@app.route('/signup')
def signup():
    form = SignUpForm()
    return render_template('signup.html', form = form)

app.run()'''