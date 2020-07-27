from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        fields = ('id', 'username', 'password')

# Init User Schema
user_schema = UserSchema()
many_user_schema = UserSchema(many=True)

# Auth
@app.route('/auth', methods=['POST'])
def auth():
    username = request.json['username']
    password = request.json['password']
    user = User.query.filter_by(username = username, password = password).first()
    result = user_schema.dump(user)

    return jsonify(result)

# Register
@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    user = User(username, password)

    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user)


# Run Server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(debug=True)