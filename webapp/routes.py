from flask import jsonify, render_template,flash, redirect, request, session, url_for
from webapp import app
from  webapp.models import Chatusers,Post,db
from sqlalchemy.exc import IntegrityError,SQLAlchemyError,DBAPIError
from webapp import socketio
from flask_socketio import  emit ,join_room,leave_room,send
from flask_login import login_user,logout_user,current_user,login_required
from webapp.form import RegistrationForm,LoginForm
import  time
from passlib.hash import pbkdf2_sha256

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if  current_user.is_authenticated:
        return render_template('home.html')
    form = LoginForm()
    user= request.method
    # print(f'\n\n{form.username.data,user}\n\n')
    if form.validate_on_submit():
        # print(f'\n\n{form.username.data}\n\n')
        uobj = Chatusers.query.filter_by(username=form.username.data).first()

        if uobj:
            u = uobj.serialize()

            if not pbkdf2_sha256.verify(form.password.data,u['password']):
                flash('Invlaid Pasword', 'danger')
            else:
                # flash('You have been logged in!', 'success')
                login_user(uobj)
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html',form=form)

@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if  current_user.is_authenticated:
        return redirect('home')
    form = RegistrationForm()

    user= request.method
    print(f'\n\n{form.username.data,user}\n\n')
    if form.validate_on_submit():
        print(f'\n\ndatabase\n\n')
        passwordhash=pbkdf2_sha256.hash(form.password.data)

        val=Chatusers(username=form.username.data,email=form.email.data,
                  password=passwordhash)
        db.session.add(val)
        db.session.commit()

        flash('Created Account login','success')
        return redirect(url_for('login'))
    else:
        print(f'\n\n{form.errors}\n\n')
        f=''
        for field ,er in form.errors.items():
            f+=str(f'*{field}  \"{er[0]}\"  ')
            print(f)
        flash(f'Unsuccessful. Please check \n{f}', 'danger')
    return redirect(url_for('login'))


@app.route("/home")
@login_required
def home():
    # print('\n\n',current_user.username)
    return render_template('home.html' ,user=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been Logged Out!!','success')
    return redirect(url_for('login'))
ROOMS=['main','game','rest']
@app.route('/chat')
@login_required
def chat():
    if  current_user.is_authenticated:
        user =current_user.username
        return render_template('chat.html',user=user,room=ROOMS)
    return redirect('login')

Main=[]
Game=[]
Rest=[]
mess=[]
loaded=[]

def adding(data,time,room):
    print('adding',time)
    if len(Post.query.filter_by(room=room).all())>100:
        print("deleting####")
        Post.query.filter_by(id=1).delete()
        # print(val)
        db.session.commit()
    val = Post(date_posted=time,content=str(data),room=room)
    # print(">>>>>",val)
    db.session.add(val)
    db.session.commit()

def fetch(room):
    print('fetching from room',room)

    uobj=Post.query.filter_by(room=room).all()

    if uobj not in loaded:
        print("in load ",room)
        loaded.append(uobj)

        for i in uobj:
            # print((i))
            date=(str(i).split('content')[0])[5:19]
            print(date)
            mes=(((str(i).split('content')[1]).split(',')[0]).split(':')[1])[2:-1]
            user=((str(i).split('content')[1]).split(',')[1].split(':')[1])[2:-1]
            room=((str(i).split('content')[1]).split(',')[2].split(':')[1])[2:-2]
            # print(mes)
            da={"msg":mes,"username":user,"room":room,"time":date}
            print(date)
            if len(eval(f'{room}')) >100:
                print(len(eval(f'{room}')))
                eval(f'{room}').pop(0)
            eval(f'{room}').append(da)

    return eval(f'{room}')

@socketio.on('input')
def message(data):
    # print(f'\n\n{data}\n\n')
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    if data['msg']:
        print("done")
        adding(data,time_stamp,data['room'])
    # eval(f'{data["room"]}').append(data)
    # print(f'\n\n{data["room"]}')

    param ={'msg':data['msg'],'username':data['username'],'room':data['room'],"time":time_stamp}
    emit('announce',param, room=data['room'])



@socketio.on('join_room')
def join(data):
    join_room(data['room'])
    param = f'{data["username"]} has Join {data["room"]} Room  '
    emit('message', param,room=data['room'])

@socketio.on('leave_room')
def leave(data):
    leave_room(data['room'])
    param=f'{data["username"]} has Leaved {data["room"]} Room   '
    emit('message',param,room=data['room'])




@socketio.on('memory')
def cache(data):
    cache=fetch(data['room'])
    # print(cache)
    # print('\n\n',data["room"],'\n\n')
    data={'cache':cache}
    emit('cache',data)