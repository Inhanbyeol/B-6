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

@app.route('/serve')
def serve():
  name = request.args.get("name")
  all_information = list(db.users.find({"name":name},{'_id':False}))

  return render_template('serve.html', info = all_information[0])


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
@app.route("/comment", methods=["POST"])
def comment_post():
    name_info = request.form['name']
    id_receive = request.form['id_give']
    comment_receive = request.form['comment_give']

    doc = {
        'name':name_info,
        'id':id_receive,
        'comment':comment_receive
    }
    db.comment.insert_one(doc)

    return jsonify({'msg': '1'})

#데이터 호출
@app.route("/comment", methods=["GET"])
def comment_get():
    all_comments = list(db.comment.find({},{'_id':False}))

    return jsonify({'result':all_comments,'msg':'get!'})

#데이터 삭제
@app.route("/comment", methods=["DELETE"])
def comment_delete():
    
    id_delete = request.form['id_delete']

    db.comment.delete_one({'id':id_delete})

    return jsonify({'msg':'1'})


#데이터 수정
@app.route("/comment", methods=["UPDATE"])
def comment_update():
    
    id_update = request.form['id_update']
    comment_update = request.form['comment_update']

    db.comment.update_one({'id':id_update},{'$set':{'comment':comment_update}})

    return jsonify({'msg':'1'})

#유저데이터 삭제
@app.route("/user", methods=["DELETE"])
def user_delete():
    
    name_delete = request.form['name_delete']

    db.users.delete_one({'name':name_delete})
    db.comment.delete_many({'name':name_delete})

    return jsonify({'msg':'1'})

#유저데이터 수정
@app.route("/user", methods=["UPDATE"])
def user_update():
    
    name_update = request.form['name_update']
    oneLine_update = request.form['oneLine_update']
    photoUrl_update = request.form['photoUrl_update']
    blogUrl_update = request.form['blogUrl_update']
    email_update = request.form['email_update']

    db.users.update_one({'name':name_update},{'$set':{'oneLine':oneLine_update,'email':email_update,'blogUrl':blogUrl_update,'photoUrl':photoUrl_update}})

    return jsonify({'msg':'1'})

if __name__ == '__main__':
  app.run('0.0.0.0', port=3000, debug=True)