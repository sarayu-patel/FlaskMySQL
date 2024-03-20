from flask import Flask,render_template,request,session
#pip install flask_mysqldb
from flask_mysqldb import MySQL
import MySQLdb.cursors
app=Flask(__name__)

#MYSQL Db configuration
app.secret_key="db4b10"
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="sarayu"
app.config["MYSQL_DB"]="db4b10"

mysql=MySQL(app)

# print(app)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login",methods=["POST","GET"])
def login():
    message=""
    if (request.method=="POST" and "uid" in request.form
         and "pass" in request.form):
        userid=request.form["uid"]
        password=request.form["pass"]
        message="logged successfully"
        return render_template("register.html" ,msg=message)
    else:
        message="enter valid details"
        return render_template("login.html",msg=message)

@app.route("/register",methods=["POST","GET"])
def register():
    message=""
    if (request.method=="POST" and "uid" in request.form
            and "pass" in request.form
        and "fn" in request.form
        and "email" in request.form
        and "gn" in request.form):
        #to get from frontend to backend
        userid=request.form["uid"]
        password= request.form["pass"]
        fullname = request.form["fn"]
        email= request.form["email"]
        gender = request.form["gn"]
        #db connection(cursor obj)
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO data values(%s,%s, %s, %s, %s)",(userid,password,fullname,email,gender))
        mysql.connection.commit()


        session['LoggedIn'] = True
        session['uid'] =userid
        session['pass'] = password
        session['fn']=fullname
        session['email']=email
        session['gn']=gender


        message="successfully account is created"
        return render_template("update.html",msg=message)
    else:
        message="Please fill the form"
        return render_template("home.html",msg=message)

@app.route("/update", methods=["GET","POST"])
def update():
    if 'uid' in session:

        userid = session['uid']
        NewPassword=request.form.get('new_pass')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("UPDATE data SET password=%s WHERE userid=%s",(NewPassword,userid))
        mysql.connection.commit()

        message = "Your account has been updated successfully"
        return render_template("update.html", msg=message)
    else:
        message ="Unauthorized access"
        return render_template("login.html",msg=message)


if __name__ == "__main__":
    app.run( debug=True)
