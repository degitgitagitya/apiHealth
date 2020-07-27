from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Init cors
CORS(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, password):
        self.username = username
        self.password = password


# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")


# Init User Schema
user_schema = UserSchema()
many_user_schema = UserSchema(many=True)

# Auth
@app.route("/auth", methods=["POST"])
def auth():
    username = request.json["username"]
    password = request.json["password"]
    user = User.query.filter_by(username=username, password=password).first()
    result = user_schema.dump(user)

    return jsonify(result)


# Register
@app.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    password = request.json["password"]
    user = User(username, password)

    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user)


# Class Drug
class Drug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    name = db.Column(db.String(100))
    information = db.Column(db.String(200))
    id_supplier = db.Column(db.Integer)

    def __init__(self, code, name, information, id_supplier):
        self.code = code
        self.name = name
        self.information = information
        self.id_supplier = id_supplier


# Drug Schema
class DrugSchema(ma.Schema):
    class Meta:
        fields = ("id", "code", "name", "information", "id_supplier")


# Init Drug Schema
drug_schema = DrugSchema()
many_drug_schema = DrugSchema(many=True)

# Get All Drug
@app.route("/drug", methods=["GET"])
def get_all_drug():
    drug = Drug.query.all()
    result = many_drug_schema.dump(drug)

    return jsonify(result)


# Create Drug
@app.route("/drug", methods=["POST"])
def add_drug():
    code = request.json["code"]
    name = request.json["name"]
    information = request.json["information"]
    id_supplier = request.json["id_supplier"]

    drug = Drug(code, name, information, id_supplier)
    db.session.add(drug)
    db.session.commit()

    return drug_schema.jsonify(drug)


# Edit Drug
@app.route("/drug/<id>", methods=["PUT"])
def update_drug(id):
    drug = Drug.query.get(id)

    drug.code = request.json["code"]
    drug.name = request.json["name"]
    drug.information = request.json["information"]
    drug.id_supplier = request.json["id_supplier"]

    db.session.commit()

    return drug_schema.jsonify(drug)


# Delete Drug
@app.route("/drug/<id>", methods=["DELETE"])
def remove_drug(id):
    drug = Drug.query.get(id)
    db.session.delete(drug)
    db.session.commit()

    return drug_schema.jsonify(drug)


# Class Supplier
class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self, code, name):
        self.code = code
        self.name = name


# Supplier Schema
class SupplierSchema(ma.Schema):
    class Meta:
        fields = ("id", "code", "name")


# Init Supplier Schema
supplier_schema = SupplierSchema()
many_supplier_schema = SupplierSchema(many=True)


# Get All Supplier
@app.route("/supplier", methods=["GET"])
def get_all_supplier():
    supplier = Supplier.query.all()
    result = many_supplier_schema.dump(supplier)

    return jsonify(result)


# Create Supplier
@app.route("/supplier", methods=["POST"])
def add_supplier():
    code = request.json["code"]
    name = request.json["name"]

    supplier = Supplier(code, name)
    db.session.add(supplier)
    db.session.commit()

    return supplier_schema.jsonify(supplier)


# Edit Supplier
@app.route("/supplier/<id>", methods=["PUT"])
def update_supplier(id):
    supplier = Supplier.query.get(id)

    supplier.code = request.json["code"]
    supplier.name = request.json["name"]

    db.session.commit()

    return supplier_schema.jsonify(supplier)


# Delete Supplier
@app.route("/supplier/<id>", methods=["DELETE"])
def remove_supplier(id):
    supplier = Supplier.query.get(id)
    db.session.delete(supplier)
    db.session.commit()

    return supplier_schema.jsonify(supplier)


# Run Server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
