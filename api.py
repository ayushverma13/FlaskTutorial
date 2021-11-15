import flask
from flask import request, jsonify
from jinja2 import Environment, FileSystemLoader
import os
from flask import Flask, jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]




@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    results = []
    for book in books:
        if book['id'] == id:
            results.append(book)
    '''    127.0.0.1:5000/api/v1/resources/books?id=0 
    127.0.0.1:5000/api/v1/resources/books?id=1 
    127.0.0.1:5000/api/v1/resources/books?id=2 
    127.0.0.1:5000/api/v1/resources/books?id=3'''
    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

contacts = [
    {'fname': 'Vaibhav',
     'phone': '123456789',
     'City': 'Pune'},
    {'fname': 'Ayush',
     'phone': '987654321',
     'City': 'Mumbai'}
]

@app.route('/email_message',methods=['GET'])
def test_message2():
    env = Environment(
        loader=FileSystemLoader(searchpath="./templates/"),variable_start_string='{{$', variable_end_string='}}')
    
    contacts=request.json["Contact"]
    template_body = env.get_template("baseemail.html")
    result=[]
    for contact in contacts:
        #if contact['fname'] == fname:
        output = template_body.render(data=contact)
        output= r"""{}""".format(output)
        output=output.replace('\n','')
        output=output.replace('\t','')
        output=output.replace('\\"','"')

        result.append({
            "Email" : output ,
        })
    
        
    return  jsonify({"Emails" : result})


@app.route('/email_message1',methods=['GET'])
def test_message1():
    env = Environment(
        loader=FileSystemLoader(searchpath="./templates/"),variable_start_string='{{$', variable_end_string='}}')
    
    contacts=request.json["Contact"]
    template=request.json["Template"]
    #template_body = env.get_template("baseemail.html")
    TEMPLATE_BODY="""
    your contact number is  {{data['phone']}}
    your city of residence is {{data['City']}}
    regards,
    {ABC Team}
    """
    TEMPLATE_HEADING ="""Dear {{data['fname']}} """
    #template_heading=env.get_template("heading.txt")
    #template_body = env.get_template("body.txt")
    template_heading= Environment().from_string(source=str(template[0]['subject']))
    template_body = Environment().from_string(source=str(template[0]['body']))

    result=[]
    for contact in contacts:

        output_heading= template_heading.render(data=contact)
        output= r"""{}""".format(output_heading)
        output=output.replace('\n','')
        output=output.replace('\t','')
        output_heading=output.replace('\\"','"')
        #print("Subject : " + output_heading)
        output_body = template_body.render(data=contact)
        output= r"""{}""".format(output_body)
        output=output.replace('\n','')
        output=output.replace('\t','')
        output_body=output.replace('\\"','"')
        #print(output)
        #print(output_body)
        result.append({
            "Body" : output_body,
            "Subject" : output_heading,

        })
    return  jsonify({"Emails" : result})


@app.route('/test_message',methods=['GET'])
def test_message():
    env = Environment(
        loader=FileSystemLoader(searchpath="./template/"),variable_start_string='{{$', variable_end_string='}}')
    contacts=request.json["Contact"]
    campaign=request.json["Campaign"]
    template=request.json["Template"]
    template_subject= Environment(variable_start_string='{{$', variable_end_string='}}').from_string(source=str(template['Subject']))
    template_body = Environment(variable_start_string='{{$', variable_end_string='}}').from_string(source=str(template['Body']))
    template_closing = Environment(variable_start_string='{{$', variable_end_string='}}').from_string(source=str(template['Closing']))
    
    result=[]
    for contact in contacts:
        temp={
            "Contact" : contact ,
            "Campaign" : campaign
            }
        output_subject =template_subject.render(data=temp)
        output= r"""{}""".format(output_subject)
        output=output.replace('\n','')
        output=output.replace('\t','')
        output_subject=output.replace('\\"','"')

        output_body =template_body.render(data=temp)
        output= r"""{}""".format(output_body)
        output=output.replace('\n','')
        output=output.replace('\t','')
        output_body=output.replace('\\"','"')

        output_closing =template_closing.render(data=temp)
        output= r"""{}""".format(output_closing)
        output=output.replace('\n','')
        output=output.replace('\t','')
        output_closing=output.replace('\\"','"')

        output = output_subject+output_body+output_closing
        
        result.append({
            "Email" : output ,
        })
    return  jsonify({"Emails" : result})

if __name__=='__main__':
    app.run(debug=True)
    

