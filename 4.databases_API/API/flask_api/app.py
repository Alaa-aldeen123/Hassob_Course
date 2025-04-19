from flask import Flask, jsonify, abort, request
import  mysql.connector


db = mysql.connector.connect(host='localhost', user='root', password='771558504', database='sakila')

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World</h1>'

@app.get('/actors')
def actors():
    query = 'SELECT actor_id, first_name, last_name FROM actor'
    results = get_results(query)
    return results

@app.get('/actors/<int:actor_id>')
def actor(actor_id):
    query = 'SELECT actor_id, first_name, last_name FROM actor WHERE actor_id = %s'
    result = get_one_result(query, (actor_id,))
    return result

@app.get('/films')
def get_films_by_rating():
    ratings = request.args['rating'].split(',')
    query_placeholders = ','.join(['%s'] * len(ratings))
    query = 'SELECT film_id, description, release_year, length, rental_rate, rating FROM film WHERE rating IN (%s)' %query_placeholders
    results = get_results(query,ratings)
    return results

#get all customers
@app.get('/customers')
def get_customers():
    query = 'SELECT customer_id, first_name, last_name FROM customer'
    results = get_results(query)
    return results

#get one customer by the first name
@app.get('/customers/<string:customer_first_name>')
def get_customer_by_name(customer_first_name):
    query = 'SELECT customer_id, first_name, last_name FROM customer WHERE first_name = %s'
    results = get_results(query,(customer_first_name,))
    return results

# get one or more customers based on their names
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_results(query, params):
    # Dummy database function: replace with actual query execution.
    return {"query": query, "params": params}


@app.get('/customers')
def get_customers_by_names():
    names_str = request.args.get('names')
    if not names_str:
        return jsonify({"error": "No names provided"}), 400

    names = [n.strip() for n in names_str.split(',') if n.strip()]
    placeholders = ','.join(['%s'] * len(names))
    query = f"SELECT customer_id, first_name, last_name FROM customer WHERE first_name IN ({placeholders})"

    results = get_results(query, tuple(names))
    return jsonify(results)




def get_results(query, *args):
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, *args)
    results = cursor.fetchall()
    cursor.close()
    return jsonify(results) if results else abort(404)

def get_one_result(query, *args):
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, *args)
    result = cursor.fetchone()
    cursor.close()
    return jsonify(result) if result else abort(404)

if __name__ == '__main__':
    app.run(debug=True)