from flask import render_template, session, request, redirect, url_for, make_response, json
from repositories import db
from werkzeug.security import generate_password_hash, check_password_hash

def account(accountmessage = ""):
    try:
        accountmessage = accountmessage
        competition = ""
        dbrows = {}
        dbcompetitions = []

        playerid = session.get("mobileno")

        if playerid is not None:
            dbcompetitions = db.getCompetitions()
            dbrows = db.getAccount(playerid)

            if len(dbrows) > 0:
                competition = dbrows["competitionname"]
            else:
                accountmessage = "Account data not found"
        else:
            accountmessage = "Please login before accessing account."

        return render_template("account.html", accountmessage=accountmessage, competitionselected=competition, dbrows=dbrows, dbcompetitions=dbcompetitions)
    except Exception as ex:
        print (ex)
        loginmessage = "Please login before changing account settings."

        return render_template("account.html", accountmessage=ex, competitionselected="", dbrows=dbrows, dbcompetitions=dbcompetitions)

        #return redirect(url_for("login", loginmessage=loginmessage))

def updateaccount():
    mobilNo = request.form.get('mobno')
    playername = request.form.get('uname')
    email = request.form.get('email')
    competition = request.form.get('competition')

    isUpdateOK = db.updateProfile(mobilNo, playername, email, competition)

    if isUpdateOK:
        session["competition"] = competition
        accountmessage = "Profile updated successfully."
    else:
        accountmessage = "Unable to update profile"

    return account(accountmessage)

def resetpassword():
    playerid = ""
    statusmessage = ""

    try:
        playerid = session.get("mobileno")

        if playerid is None:
            statusmessage = "Please login to reset password"
    except Exception as ex:
        print ("Error: ", ex)
        statusmessage = "Unable to load data."
    
    return render_template("resetpass.html", resetpassmessage=statusmessage, playerid=playerid)

        #return redirect(url_for('forgetpassword', resetpassmessage=resetpassmessage, competitionselected="", dbrows=None, dbcompetitions=None))

def updatepassword():
    mobileNo = session.get("mobileno")
    passwd = request.form.get('opsw')
    npasswd1 = request.form.get('npsw1')
    npasswd2 = request.form.get('npsw2')
    statusmessage = ""

    if mobileNo is None:
        statusmessage = "Please login to update password"
    else:
        if npasswd1 != npasswd2:
            statusmessage = "New password does not match"
        else:
            playenrname, competition, playerpwd = db.CheckLogin(mobileNo)

            if len(playenrname) > 0:
                if check_password_hash(playerpwd, passwd):
                    isUpdateOK = db.UpdatePassword(mobileNo, generate_password_hash(npasswd1))
                    
                    if isUpdateOK > 0:
                        statusmessage = "Password updated successfully. Login with your new password"
                        return redirect(url_for('login', loginmessage=statusmessage))
                    else:
                        statusmessage = "Invalid Login/Password. Password could not be updated"
                else:
                    statusmessage = "Invalid Login/Password. Password could not be updated"

    #return make_response(redirect(url_for('resetpassword', resetpassmessage=statusmessage)))
    return render_template("resetpass.html", resetpassmessage=statusmessage, playerid=mobileNo)
