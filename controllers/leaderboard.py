from flask import render_template, session
from repositories import db

def leaderboard():
    playerid = ""
    statusmessage = ""
    competition = ""
    dbrows = []

    try:
        playerid = session.get("mobileno")
        
        if playerid is None:
            statusmessage = "Please login to view your score"
        else:
            competition = session.get("competition")
            if competition is None:
                statusmessage = "Please set default competition to view your score"
            else:
                #isSubmitted = db.isSubmitted(playerid, competition)
                #if not isSubmitted:
                #    statusmessage = "Score cannot be viewed until all responses are submitted"
                #else:
                #    dbrows = db.getScore(playerid)
                dbrows = db.getScore(playerid)
    except Exception as ex:
        print ("leaderboard:", ex)
        statusmessage = "Unable to load data."
    
    return render_template("leaderboard.html", reportMessage=statusmessage, dbrows=dbrows)

def ranks():
    dbrows = db.getRanks()
    return render_template("rankreport.html", dbrows=dbrows)