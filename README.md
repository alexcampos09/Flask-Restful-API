This is my solution for a coding challenge I received. The instructions are written in the PDF file.

I solved it by working out the logic first using a Jupyter Notebook with Python and Pandas. Later I implemented an API using
SQLite and the Flask Framework.

To run it in your machine you will need to install the libraries from the requirements.txt file.
It is advisable to set up a Virtual Environment before you install the libraries.

Follow these steps:

1 - Clone the repo and use `pip install virtualenv` if you don't have it yet

2 - Inside of the directory Flask-Restful-API, run: `virtualenv venv`

3 - Activate the Virtual Environmet: `source venv/bin/activate`

4 - To install all the necessary libraries run: `pip install -r requirements.txt`

5 - Change to the app directory: `cd rest-app` 

6 - Run the application: `flask run`

Now just go this url: http://127.0.0.1:5000/
There you can try the following combinations on the url (after the word 'string:') to query different types of coffe machines and coffe podes from the api:

machine_type = ['Small', 'Large', 'Espresso']

flavor = ['vanilla', 'caramel', 'psl', 'mocha', 'hazelnut']

/coffee-machine/<string:machine_type>/

/coffee-pods/<string:machine_type>/

/coffee-pods/<string:machine_type>/<string:flavor>/

/coffee-pods/<string:machine_type>/smallest-by-machine/

/coffee-pods/<string:flavor>/smallest-by-flavor/
