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
    result = db.users.insert_one({"photoUrl" : info['photoUrl'], "name" : info['name'], "email" : info['email'], "blogUrl" : info['blogUrl'], "oneLine" : info['oneLine']})

    if result.acknowledged == True :
       return jsonify(1)
    else :
       return jsonify(0)

#정보 출력
@app.route("/user", methods=["GET"])
def create_get():
    all_comments = list(db.users.find({},{'_id':False}))

    return jsonify({'result':all_comments,'msg':'get!'})

#데이터 저장
@app.route("/testc", methods=["POST"])
def testc_post():
    name_info = request.form['name']
    id_receive = request.form['id_give']
    comment_receive = request.form['comment_give']

    doc = {
        'name':name_info,
        'id':id_receive,
        'comment':comment_receive
    }
    db.testc.insert_one(doc)

    return jsonify({'msg': '1'})

#데이터 호출
@app.route("/testc", methods=["GET"])
def testc_get():
    all_comments = list(db.testc.find({},{'_id':False}))

    return jsonify({'result':all_comments,'msg':'get!'})


if __name__ == '__main__':
  app.run('0.0.0.0', port=3000, debug=True)