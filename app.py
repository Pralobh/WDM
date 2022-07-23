
from hashlib import new
from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///login.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Login(db.Model):
    userid=db.Column(db.String(20),primary_key=True)
    password=db.Column(db.String(20),nullable=False)
    usertype=db.Column(db.String(5),nullable=False)
    datecreated=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.userid} -- {self.password} -- {self.usertype}"

@app.route('/',methods=['GET','POST'])
def hello():
    if request.method=="POST":
        # print("post method here")
        userid=request.form['userid']
        password=request.form['password']
        usertype=request.form['usertype']
        todo=Login(userid=userid,password=password,usertype=usertype)
        db.session.add(todo)
        db.session.commit()
    allinfo=Login.query.all()
    return render_template('index.html',allinfo=allinfo)
    
@app.route('/delete/<userid>')
def delete(userid):
    rec=Login.query.filter_by(userid=userid).first()
    db.session.delete(rec)
    db.session.commit()
    return redirect("/")
    
@app.route('/update/<userid>',methods=['GET','POST'])
def update(userid):
    if request.method=="POST":
        newrec=Login.query.filter_by(userid=userid).first()
        userid=request.form['userid']
        password=request.form['password']
        usertype=request.form['usertype']
        newrec.userid=userid
        newrec.password=password
        newrec.usertype=usertype
        db.session.add(newrec)
        db.session.commit()
        return redirect("/")

    rec=Login.query.filter_by(userid=userid).first()
    return render_template('update.html',info=rec)

if __name__=="__main__":
    app.run(debug=True,port=5000)