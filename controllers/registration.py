from flask import render_template, request, make_response, redirect, url_for, session
from repositories import db
from werkzeug.security import generate_password_hash

#@app.route('/signup')
def signup():
    dbrows = db.getCompetitions()
    competition = request.args.get("competition")
    return render_template("registration.html", competitionselected=competition, registrationmessage="", dbrows=dbrows)

#@app.route('/senddetails')
def register():
    competition = request.form.get('competition')
    name = request.form.get('uname')
    email = request.form.get('email')
    passwd = generate_password_hash(request.form.get('psw'))
    mobilNo = request.form.get('mobno')

    isRegistrationOK = db.registerPlayer(name, email, passwd, mobilNo, competition)

    if isRegistrationOK:
        loginmessage = "Registration completed successfully. Login with your mobile number and password."
        #return render_template("login.html")
        session["competition"] = competition
        session["playername"] = name
        resp = redirect(url_for("login", loginmessage=loginmessage))
        return resp
    else:
        return render_template("registration.html", registrationmessage="Unable to register..")

def genpass():
    #competition = request.form.get('competition')
    mobilNo = request.args.get('playerid')
    newpassmessage = request.args.get('newpassmessage')
    
    return render_template("newpass.html", newpassmessage=newpassmessage, playerid=mobilNo)

def newpassupdate():
    mobileNo = request.form.get("mobno")
    usrotp = request.form.get('otp')
    npasswd1 = request.form.get('npsw1')
    npasswd2 = request.form.get('npsw2')
    statusmessage = ""

    if mobileNo is None:
        statusmessage = "Invalid mobile number or mobile number not found"
    else:
        if npasswd1 != npasswd2:
            statusmessage = "New password does not match"
        else:
            isOTPOK = db.IsOTPValid(mobileNo, usrotp)

            if isOTPOK:
                isUpdateOK = db.UpdatePassword(mobileNo, generate_password_hash(npasswd1))
                
                if isUpdateOK > 0:
                    statusmessage = "Password updated successfully. Login with your new password"
                    return redirect(url_for('login', loginmessage=statusmessage))
                else:
                    statusmessage = "Invalid Login/Password. Password could not be updated"
            else:
                statusmessage = "OTP does not match"
    
    return redirect(url_for('genpass', newpassmessage=statusmessage, player_id=mobileNo))
