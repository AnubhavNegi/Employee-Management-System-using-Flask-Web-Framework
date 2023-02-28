from flask import Flask, render_template, request,url_for

app=Flask(__name__)

@app.route('/')
def signin():
    return render_template('admin_login.html')

@app.route('/signin', methods=['POST'])
def login():
    import sqlite3
    email = request.form['userid']
    pwd = request.form['pwd']
    try:
        con=sqlite3.connect('login.db')
        cur=con.cursor()
        data=cur.execute('select * from login where id=(?)',[email])
        result=data.fetchone()
        if result == None:
            return render_template('admin_login.html')
        else:
            if result[1] == pwd:
                return render_template('index.html')
            else:
                return render_template('admin_login.html')
    except:
        return render_template('error.html')
    finally:
        con.commit()
        con.close()

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/delete')
def delete():
    return render_template('delete.html')

@app.route('/savedetails',methods=['POST'])
def savedetails():
    msg=""
    if request.method=='POST':
        try:
            import sqlite3
            name=request.form['name']
            email=request.form['email']
            add=request.form['address']
            con=sqlite3.connect('cetpa.db')
            cursor=con.cursor()
            cursor.execute("insert into emp values(?,?,?)",[name,email,add])
            con.commit()
            return render_template('success.html',msg="Record Added Successfully")
        except:
            return render_template('success.html',msg="Error!!!")
        finally:
            con.close()

@app.route("/view")
def view():
    import sqlite3
    con=sqlite3.connect("cetpa.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from emp")
    rows=cur.fetchall()
    return render_template("view.html",rows=rows)

@app.route("/deleterecord",methods=["POST"])
def deleterecord():
    msg=""
    import sqlite3
    email=request.form['email']
    try:
        with sqlite3.connect("cetpa.db") as con:
                cur=con.cursor()
                r = cur.execute('select * from emp where email=(?)', [email])
                flag = r.fetchone()
                if flag != None:
                    cur.execute("delete from emp where email=(?)",[email])
                    msg = 'Record deleted'
                else:
                    msg = "Record doesn't exist"
    except:
        msg = "An error has occured"
    finally:
        return render_template("delete_record.html",msg=msg)

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/updatedetails', methods=['POST'])
def updatedetails():
    msg=''
    import sqlite3
    name=request.form['name']
    email=request.form['email']
    add=request.form['address']
    with sqlite3.connect('cetpa.db') as con:
        cur=con.cursor()
        r=cur.execute('select * from emp where email=(?)',[email])
        result=r.fetchone()
        if result == None:
            msg="Record doesn't exist"
        else:
            cur.execute("update emp set name='"+name+"', address='"+add+"' where email='"+email+"'")
            msg='Record successfully updated'
    return render_template('update_record.html',msg=msg)
app.run(debug=True)