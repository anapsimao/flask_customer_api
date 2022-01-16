from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# initial appSolicitation

app = Flask(__name__)

# dataBase

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:91775667@localhost:5433/customers'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initial dataBase

db = SQLAlchemy(app)

# initial marshmallow

ma = Marshmallow(app)

# customer register model


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(255))
    address = db.Column(db.String(255))
    role = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))

    def __init__(self, name, age, gender, address, role, email, phone_number):
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address
        self.role = role
        self.email = email
        self.phone_number = phone_number


# customer schema

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'gender', 'address',
                  'role', 'email', 'phone_number')

# initial schema


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


@app.route('/', methods=['GET'])
def get():
    return jsonify({'msg': 'hello world, I am working'})

# create customer


@app.route('/customer', methods=['POST'])
def add_customer():
    name = request.json['name']
    age = request.json['age']
    gender = request.json['gender']
    address = request.json['address']
    role = request.json['role']
    email = request.json['email']
    phone_number = request.json['phone_number']
    new_customer = Customer(name, age, gender, address,
                            role, email, phone_number)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer)

# get all customers


@app.route('/customers', methods=['GET'])
def get_customers():
    all_customers = Customer.query.all()
    result = customers_schema.dump(all_customers)
    return jsonify(result)

# get single customer


@app.route('/customer/<id>', methods=['GET'])
def get_customer(id):
    customer_get = Customer.query.get(id)
    return customer_schema.jsonify(customer_get)

# modify all data customer


@app.route('/customer/<id>', methods=['PUT'])
def put_customer(id):
    customer = Customer.query.get(id)
    name = request.json['name']
    age = request.json['age']
    gender = request.json['gender']
    address = request.json['address']
    role = request.json['role']
    email = request.json['email']
    phone_number = request.json['phone_number']
    customer.name = name
    customer.age = age
    customer.gender = gender
    customer.address = address
    customer.role = role
    customer.email = email
    phone_number = phone_number
    db.session.commit()
    return customer_schema.jsonify(customer)


# update some details Customer


# @app.route('/customer/<id>', methods=['PATCH'])
# def update_customer(id):


# Delete Customer


@app.route('/customer/<id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()
    return customer_schema.jsonify(customer)

# Run Server


if __name__ == '__main__':
    app.run(debug=True)
