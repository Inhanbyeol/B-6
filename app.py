from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://b6:TEJ6JD6Xn9IxLfLg@cluster0.3ptd6x1.mongodb.net/?retryWrites=true&w=majority')
db = client.data

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/create')
def create():
  return render_template('create.html')

@app.route("/create", methods=["POST"])
def createUsers():
    info = request.get_json()
    db.users.insert_one({"photoUrl" : info['photoUrl'], "name" : info['name'], "email" : info['email'], "blogUrl" : info['blogUrl'], "oneLine" : info['oneLine']})
    
    return jsonify(1)

if __name__ == '__main__':
  app.run('0.0.0.0', port=3000, debug=True)