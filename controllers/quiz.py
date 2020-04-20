from flask import render_template, request, session
import datetime
from repositories import db
import flask

def question():
    player_id = session.get("mobileno")
    if player_id is None:
        quizmessage = "Please Login to play."
        return render_template("quiz.html", playername="", questionmessage=quizmessage, dbqna={}, maxqcount="")

    competition_name = session["competition"]
    player_name = session["playername"]
    max_question_count = ""
    db_question_list = []

    current_quiz_qna = db.getQuizQuestion(player_id, competition_name)
    # print (current_quiz_qna)

    if len(current_quiz_qna) == 0:
        quizmessage = "No active question. Please try again later."
    else:
        max_question_count = db.getQuestionCount(competition_name)
        
        quizmessage = "Current active question."

    dbqlist = db.getQuestionList(player_id, competition_name)
    #print (player_id, competition_name)
    

    return render_template("quiz.html", playername=player_name, questionmessage=quizmessage, dbqna=current_quiz_qna, maxqcount=max_question_count, dbqlist=dbqlist)

def thisQuestion(qno):
    #player_id = request.cookies.get("playerid")
    player_id = session.get("mobileno")
    if player_id is None:
        quizmessage = "Please Login to play."
        return render_template("quiz.html", playername="", questionmessage=quizmessage, dbqna={}, maxqcount="")

    competition_name = session["competition"]
    player_name = session["playername"]
    max_question_count = ""
    dbqlist = []

    current_quiz_qna = db.getThisQuizQuestion(player_id, competition_name, qno)
    
    if len(current_quiz_qna) == 0:
        quizmessage = "No active question. Please try again later."
    else:
        max_question_count = db.getQuestionCount(competition_name)
        quizmessage = "Current active question."

    dbqlist = db.getQuestionList(player_id, competition_name)
    
    return render_template("quiz.html", playername=player_name, questionmessage=quizmessage, dbqna=current_quiz_qna, maxqcount=max_question_count, dbqlist=dbqlist)

def answersave():
    player_id = session["mobileno"]
    competition_name = session["competition"]
    max_question_count = ""

    qid = request.form.get("qid")
    qdesc = request.form.get("qdesc")
    points = request.form.get("points")
    ans = request.form.get("choice")
    negativepoints = request.form.get("negativepoints")

    resptime = datetime.datetime.now()

    questionmessage = ""

    #isResponded = db.isResponded(player_id, qid)
    isSubmitted = db.isSubmitted(player_id, competition_name)

    if isSubmitted == True:
        questionmessage = "You have already submitted response. Response cannot be changed."
    else:
        correct_ans = db.getAnswer(competition_name, qid)

        if correct_ans != ans:
            points = negativepoints

        isRegisterOK = db.registerResponse(player_id, competition_name, qid, qdesc, ans, resptime, points)

        if isRegisterOK:
            questionmessage = "Your response registered successfully"
        else:
            questionmessage = "Unable to register response."

    current_quiz_qna = db.getQuizQuestion(player_id, competition_name)

    if not bool(current_quiz_qna.items):
        questionmessage = "No more active question at this time.."
    else:
        max_question_count = db.getQuestionCount(competition_name)

    dbqlist = db.getQuestionList(player_id, competition_name)
    return render_template("quiz.html", questionmessage=questionmessage, dbqna=current_quiz_qna, maxqcount=max_question_count, dbqlist=dbqlist)

def submit():
    player_id = session["mobileno"]
    competition_name = session["competition"]

    max_question_count = ""

    questionmessage = ""

    isSubmitted = db.isSubmitted(player_id, competition_name)

    if isSubmitted == True:
        questionmessage = "You have already submitted response. Response cannot be submitted again."
    else:
        subtime = datetime.datetime.now()

        isSubmitOK = db.submitResponse(player_id, competition_name, subtime)

        if isSubmitOK:
            questionmessage = "Your responses submitted successfully"
        else:
            questionmessage = "Unable to submit responses."

    current_quiz_qna = db.getQuizQuestion(player_id, competition_name)

    if not bool(current_quiz_qna.items):
        questionmessage = "No more active question at this time.."
    else:
        max_question_count = db.getQuestionCount(competition_name)

    dbqlist = db.getQuestionList(player_id, competition_name)
    return render_template("quiz.html", questionmessage=questionmessage, dbqna=current_quiz_qna, maxqcount=max_question_count, dbqlist=dbqlist)
