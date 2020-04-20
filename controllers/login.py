from flask import render_template, request, make_response, redirect, url_for, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from repositories import db
from common import utility

#@app.route('/login')
def login():
    loginmessage = request.args.get('loginmessage')

    if loginmessage is None:
        loginmessage = ""
    
    return render_template("login.html", loginmessage=loginmessage)

#@app.route('/adminlogin')
def adminlogin():
    email = request.args.get('inp_email')
    passwd = request.args.get('inp_pass')
    if email == "pkh_p@hotmail.com" and passwd == "pkh1234":
        return render_template("addQuestion.html")
    else:
        return render_template("admin.html", success="Invalid email/password")

#@app.route('/loginsubmit', methods=['POST', 'GET'])
def chklogin():
    mobileNo = request.form.get('uname')
    passwd = request.form.get('psw')
    remember = request.form.get('remember')

    playenrname, competition, playerpwd = db.CheckLogin(mobileNo)
    if len(playenrname) > 0:
        if check_password_hash(playerpwd, passwd):    
            session["mobileno"] = mobileNo
            session["competition"] = competition
            session["playername"] = playenrname

            questionmessage = "You are logged in"
            resp = make_response(redirect(url_for("question", questionmessage=questionmessage)))
            
            if (remember == "on"):
                resp.set_cookie("playerid", mobileNo, max_age=1)
            
            return resp
        else:
            return render_template("login.html", loginmessage="Invalid mobile number/password")
    else:
        return render_template("login.html", loginmessage="Invalid mobile number/password")
    
def forgotpass():
    return render_template("forgotpass.html", resetpassmessage="")

def genotp():
    newpassmessage = ""
    competitionselect = ""

    mobileNo = request.form.get('mobno')
    otpnum = utility.generateOTP()
    otpmsg = otpnum + " is your One Time Password to reset password. It isvalied for 5 min."
    isSendOTPOK = utility.sendOTP(mobileNo, otpmsg)

    if isSendOTPOK:
        otpvalidtilltime = datetime.datetime.now() + datetime.timedelta(minutes=5)
        isSaveOTPOK = db.saveOTP(mobileNo, otpnum, otpvalidtilltime)

        if isSaveOTPOK:
            session["mobileno"] = mobileNo
            #dbrows = db.getCompetitions()
            newpassmessage = "OTP sent. Please check your mobile."
        else:
            newpassmessage = "Unable to send OTP.."
    else:
        newpassmessage = "Error while sending OTP.."
    
    return redirect(url_for('genpass', newpassmessage=newpassmessage, playerid=mobileNo))