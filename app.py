from flask import Flask,request,redirect,url_for,render_template,make_response
app=Flask(__name__)
userdata={}
linkdata={}
@app.route('/')
def home():
    return render_template('welcome.html')


#REGISTER
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form.get('uname')
        userpassword=request.form.get('upassword')
        useremail=request.form.get('uemail')

        if username not in userdata:
            linkdata[username]=[]
            userdata[username]={'password':userpassword,'email':useremail}
            return redirect(url_for('login'))
        else:
            return 'Username already Existed'

    return render_template('register.html')


#LOGIN
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        log_uname=request.form.get('uname')  #ankitha
        log_password=request.form.get('upassword') #asd

        if log_uname in userdata:
            if userdata[log_uname]['password']==log_password:
 
                    resp=make_response(redirect(url_for('dashboard')))
                    resp.set_cookie('userdata',log_uname)
                    return resp

            else:
                return 'password is Wrong'
        else:
            return 'Username doesnt exist!!'
    return render_template('login.html')


#DASHBOARD
@app.route('/dashboard')
def dashboard():
    if request.cookies.get('userdata'):
        username=request.cookies.get('userdata')
        link_data=linkdata[username]
        link1=None
        link2=None
        if len(linkdata[username])>0:
            link1=linkdata[username][-1]
        if len(linkdata[username])>1:
            link2=linkdata[username][-2]

        return render_template('dashboard.html',user_name=username,link_data=link_data,link1=link1,link2=link2)
    else:
        return 'Please Login!!'


#ADD PAGE
@app.route('/add', methods=["GET", "POST"])
def add():
    if request.cookies.get('userdata'):
        username = request.cookies.get('userdata')

        if request.method == 'POST':
            add_name = request.form.get('urlname')
            add_url = request.form.get('url')

            add_data = [add_name, add_url]
            
            linkdata[username].append(add_data)

            return redirect(url_for('view'))

        return render_template('add.html')   
    else:
        return redirect(url_for('login'))
    

#VIEW PAGE
@app.route('/view', methods=['GET', 'POST'])
def view():
    if request.cookies.get('userdata'):
        username = request.cookies.get('userdata')

        #DELETE
        if request.method == "POST" and "delete" in request.form:
            index = int(request.form.get("delete"))
            del linkdata[username][index]      
            return redirect(url_for('view'))   

        #EDIT
        if request.method == "POST" and "urlname" not in request.form and "delete" not in request.form:
            index = int(request.form.get("index"))
            name, url = linkdata[username][index]

            return render_template("edit.html", index=index, name=name, url=url)

        #UPDATE
        if request.method == "POST" and "urlname" in request.form:
            index = int(request.form.get("index"))
            new_name = request.form.get("urlname")
            new_url = request.form.get("url")

            linkdata[username][index] = [new_name, new_url]
            return redirect(url_for('view'))

        #DEFAULT VIEW PAGE
        links = linkdata[username]
        return render_template('view.html', links=links)

    return redirect(url_for('login'))

#LOGOUT
@app.route('/logout')
def logout():
    if request.cookies.get('userdata'):
        username=request.cookies.get('userdata')
        resp=make_response(redirect(url_for('home')))
        resp.delete_cookie('userdata')
        return resp
    else:
        return redirect(url_for('register'))
    

#DELETE ACCOUNT
@app.route('/delete_acc', methods=['GET','POST'])
def delete_acc():
    if request.cookies.get('userdata'):
        username = request.cookies.get('userdata')

        if request.method == 'GET':
            return render_template('delete.html', username=username)

        if request.method == 'POST':
            del_pass = request.form.get('delpass')
            org_pass = userdata[username]['password']

            if del_pass == org_pass:
                userdata.pop(username)
                linkdata.pop(username)

                resp = make_response(redirect(url_for('home')))
                resp.delete_cookie('userdata')
                return resp

            # Wrong password
            return render_template('delete.html', username=username)

    # No cookie → not logged in
    return redirect(url_for('home'))

    

    
app.run(use_reloader=True,debug=True)