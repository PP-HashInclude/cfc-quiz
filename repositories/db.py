from common import config
import sqlite3
import csv

dbfile = config.getdbfile()

def opendb():
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    return conn, c

def calculateRanks(rows):

    #row_lst = []
    newrows = []
    name_idx = 0
    competitionname_idx = 1
    totalpoints_idx = 2
    rank_idx = 3
    time_index = 4

    curr_rank = 1
    for row in range(len(rows)):
        if row == 0:
            #row_lst.append(1)
            curr_competition = rows[row][competitionname_idx]
            t1 = (rows[row][name_idx], rows[row][competitionname_idx],
                      rows[row][totalpoints_idx], curr_rank, rows[row][time_index])
            newrows.append(t1)
            continue

        if rows[row][competitionname_idx] != curr_competition:
            curr_competition = rows[row][competitionname_idx]
            curr_rank = 1
            t1 = (rows[row][name_idx], rows[row][competitionname_idx],
                      rows[row][totalpoints_idx], curr_rank, rows[row][time_index])
            newrows.append(t1)
            continue

        if rows[row][totalpoints_idx] == rows[row-1][totalpoints_idx]:
            if rows[row][time_index] == rows[row-1][time_index]:
                #row_lst.append(curr_rank)
                t1 = (rows[row][name_idx], rows[row][competitionname_idx],
                        rows[row][totalpoints_idx], curr_rank, rows[row][time_index])
                newrows.append(t1)
                continue
            else:
                curr_rank += 1
                t1 = (rows[row][name_idx], rows[row][competitionname_idx],
                        rows[row][totalpoints_idx], curr_rank, rows[row][time_index])
                newrows.append(t1)
        else:
            curr_rank += 1
            t1 = (rows[row][name_idx], rows[row][competitionname_idx],
                    rows[row][totalpoints_idx], curr_rank, rows[row][time_index])
            newrows.append(t1)
    
    return newrows

def quote_fix(string):
    new_string = ""
    for i in range(len(string)):
        if string[i] == "'":
            new_string += "'"
        new_string += string[i]
    return new_string

def getQuestionCount(competition_name):
    conn,  cur = opendb()
    sql = "SELECT max(qid) as maxqcount FROM QuestionBank WHERE CompetitionName = '" + competition_name + "'"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    rowDict = {}
    maxqcount = 0

    if len(rows) > 0:
        maxqcount = rows[0][0]

    return maxqcount

def getQuizQuestion(playerid, competition_name):
    con, cur = opendb()
    
    strSql = "SELECT QId, Quesdesc, Choice1,Choice2,Choice3,Choice4,ValidTill,Points,NegativePoints, \
        (SELECT ResponseChoice from PlayerResponse pr2 where pr2.QId = QuestionBank.QId AND pr2.PlayerId = " + playerid + "  AND \
                            pr2.competitionname = QuestionBank.competitionname) As ResponseChoice \
        FROM QuestionBank \
        WHERE CompetitionName = '" + competition_name + "' AND \
            datetime(ValidTill) > datetime('now') AND \
            QId not in (SELECT QId \
                        FROM PlayerResponse \
                        WHERE PlayerResponse.QId = QuestionBank.QId AND \
                            PlayerResponse.competitionname = QuestionBank.competitionname AND \
                            PlayerResponse.SubmittedOn IS NULL AND \
                            PlayerResponse.PlayerId = " + playerid + ") \
        ORDER BY datetime(ValidTill) ASC LIMIT 1"

    cur.execute(strSql)
    rows = cur.fetchall()
    
    if len(rows) == 0:
        strSql = "SELECT QId, Quesdesc, Choice1,Choice2,Choice3,Choice4,ValidTill,Points,NegativePoints, \
                    (SELECT ResponseChoice from PlayerResponse pr2 where pr2.QId = QuestionBank.QId AND pr2.PlayerId = " + playerid + "  AND \
                                        pr2.competitionname = QuestionBank.competitionname) As ResponseChoice \
                    FROM QuestionBank \
                    WHERE CompetitionName = '" + competition_name + "' AND \
                        datetime(ValidTill) > datetime('now') AND \
                        QId in (SELECT QId \
                                    FROM PlayerResponse \
                                    WHERE PlayerResponse.QId = QuestionBank.QId AND \
                                        PlayerResponse.competitionname = QuestionBank.competitionname AND \
                                        PlayerResponse.SubmittedOn IS NULL AND \
                                        PlayerResponse.PlayerId = " + playerid + ") \
                    ORDER BY datetime(ValidTill) ASC LIMIT 1"
        cur.execute(strSql)

        rows = cur.fetchall()
    
    # print (strSql)

    cur.close()
    con.close()

    qid = ""
    qdesc = ""
    ch1 = ""
    ch2 = ""
    ch3 = ""
    ch4 = ""
    validtill = ""
    points = ""
    negativepoints = ""
    responsechoice = ""

    rowDict = {}
    
    for item in rows:
        qid = item[0]
        qdesc = item[1]
        ch1 = item[2]
        ch2 = item[3]
        ch3 = item[4]
        ch4 = item[5]
        validtill = item[6]
        points = item[7]
        negativepoints = item[8]
        responsechoice = item[9]
    
        rowDict = {"qid": qid,
                    "qdesc": qdesc,
                    "ch1": ch1,
                    "ch2": ch2,
                    "ch3": ch3,
                    "ch4": ch4,
                    "validtill": validtill,
                    "points": points,
                    "negativepoints": negativepoints,
                    "responsechoice": responsechoice
                    }
    
    return rowDict

def getThisQuizQuestion(playerid, competition_name, qno):
    con, cur = opendb()
    
    strSql = "SELECT qb.QId, qb.Quesdesc, qb.Choice1, qb.Choice2, qb.Choice3, qb.Choice4, qb.ValidTill, qb.Points, qb.NegativePoints, pr.ResponseChoice \
                FROM QuestionBank qb LEFT OUTER JOIN PlayerResponse pr ON pr.QId = qb.QId AND pr.PlayerId = " + playerid + " \
                WHERE qb.QId = " + qno + " AND \
                qb.CompetitionName = '" + competition_name + "' AND \
                datetime(qb.ValidTill) > datetime('now')"
    
    # print ("getthisquizquestion", strSql)
    cur.execute(strSql)

    rows = cur.fetchall()
    
    cur.close()
    con.close()

    qid = ""
    qdesc = ""
    ch1 = ""
    ch2 = ""
    ch3 = ""
    ch4 = ""
    validtill = ""
    points = ""
    negativepoints = ""
    responsechoice = ""

    rowDict = {}
    
    for item in rows:
        qid = item[0]
        qdesc = item[1]
        ch1 = item[2]
        ch2 = item[3]
        ch3 = item[4]
        ch4 = item[5]
        validtill = item[6]
        points = item[7]
        negativepoints = item[8]
        responsechoice = item[9]
    
        rowDict = {"qid": qid,
                    "qdesc": qdesc,
                    "ch1": ch1,
                    "ch2": ch2,
                    "ch3": ch3,
                    "ch4": ch4,
                    "validtill": validtill,
                    "points": points,
                    "negativepoints": negativepoints,
                    "responsechoice": responsechoice
                    }
    
    return rowDict

def isSubmitted(player_id, competition_name):
    isallrespsubmitted = False
    
    try:
        conn, cur = opendb()
    
        #sql = "SELECT qb.QId, qb.competitionname \
        #        FROM PlayerResponse pr, QuestionBank qb \
        #        WHERE PlayerId = " + player_id + " AND  \
        #            qb.competitionname = '" + competition_name + "' AND \
        #            qb.Qid = pr.QId AND  \
        #            pr.SubmittedOn IS NOT NULL"
        sql = "SELECT (SELECT count(QId) \
            FROM PlayerResponse pr \
            WHERE PlayerId = " + player_id + " AND \
                competitionname = '" + competition_name + "' AND \
                SubmittedOn IS NOT NULL) = \
                        (SELECT count(QId) \
                        FROM QuestionBank qb \
                        WHERE qb.competitionname = '" + competition_name + "') AS IsRowPresent"

        cur.execute(str(sql))
        dbrows = cur.fetchall()

        conn.commit()

        cur.close()
        conn.close()

        if len(dbrows) > 0:
            isrecordFound = dbrows[0][0]
            if isrecordFound == 1:
                isallrespsubmitted = True
                
    except Exception as ex:
        print("issubmitted", ex)
        #pass
    
    return isallrespsubmitted

def submitResponse(player_id, competition_name, subtime):
    issubmitOK = False
    try:
        conn, cur = opendb()

        sql = "INSERT INTO PlayerResponse (PlayerId, competitionname, QId, Question, ResponseChoice, RespondedOn, Points, SubmittedOn) \
            SELECT " + player_id + " AS PlayerId, \
                '" + competition_name + "' As competitionname, \
                    qb.QId, qb.Quesdesc, \
                    NULL AS ResponseChoice, \
                    datetime('now') AS RespondedOn, \
                    0 AS Points, \
                    '" + str(subtime) + "' AS SubmittedOn \
            FROM QuestionBank qb \
            WHERE CompetitionName = '" + competition_name + "' \
                AND QId NOT IN (SELECT QId \
                				FROM PlayerResponse pr \
                                WHERE PlayerId = " + player_id + " AND \
                                    qb.Qid = pr.QId)"
        
        # print ("insert:", sql)

        cur.execute(str(sql))
        conn.commit()

        sql = "UPDATE PlayerResponse SET SubmittedOn = '" + str(subtime) + "' WHERE PlayerId = " + str(player_id) + " AND CompetitionName = '" + competition_name + "' AND SubmittedOn IS NULL"

        #print ("update:", sql)

        cur.execute(str(sql))
        conn.commit()

        cur.close()
        conn.close()

        issubmitOK = True    
    except Exception as ex:
        print("submitResponse", ex)
        #pass
    
    return issubmitOK


def createQuestion(qno, ques_desc, choice1, choice2, choice3, choice4, choice_right, valid_till):
    conn, cur = opendb()
    
    sql = "INSERT INTO QuestionBank VALUES (" + str(qno) + ",'" + quote_fix(str(choice1)) + "','" + quote_fix(str(choice2)) + "','" + quote_fix(str(choice3)) + "','" + quote_fix(str(choice4)) + "','" + quote_fix(str(choice_right)) + "','" + quote_fix(str(ques_desc)) + "', datetime('" + str(valid_till) + "'))"

    cur.execute(str(sql))
    
    conn.commit()

    cur.close()
    conn.close()

def CheckLogin(loginid):
    sql = "SELECT name, competitionname, password FROM Players WHERE mobile = " + str(loginid)
    
    conn, cur = opendb()

    cur.execute(sql)
    rows = cur.fetchall()

    cur.close()
    conn.close()

    if len(rows) > 0:
        playername = rows[0][0]
        competition = rows[0][1]
        playerpwd = rows[0][2]
    else:
        playername = ""
        competition = ""
        playerpwd = ""
    
    return playername, competition, playerpwd

def registerPlayer(name, email, passwd, mobileNo, competitionname):
    isRegistrationOK = False
    try:
        conn, cur = opendb()
    
        sql = "INSERT INTO Players VALUES ('" + str(name) + "','" + str(email) + "','" + str(passwd) + "', " + mobileNo + ", '" + str(competitionname) + "')"

        cur.execute(str(sql))

        conn.commit()

        cur.close()
        conn.close()

        isRegistrationOK = True
    except Exception as ex:
        print("registerPlayer", ex)
        #pass
    
    return isRegistrationOK

def getCompetitions():
    sql = "SELECT Name FROM competition WHERE datetime('now') < datetime(EndingOn)"

    conn, cur = opendb()

    cur.execute(sql)
    dbrows = cur.fetchall()

    cur.close()
    conn.close()

    return dbrows

def getQuestionList(playerid, competitionname):
    #sql = "SELECT qb.QId, CASE WHEN pr.QId IS NULL THEN 'not saved' ELSE 'saved' END AS saved \
    #    FROM QuestionBank qb LEFT OUTER JOIN PlayerResponse pr ON qb.QId = pr.QId AND \
    #        pr.PlayerId = " + playerid + " \
    #    WHERE qb.competitionname = '" + competitionname + "'"
    sql = "SELECT qb.QId, CASE WHEN (SELECT pr.qid \
                                    FROM PlayerResponse pr \
                                    WHERE pr.QId = qb.qid AND \
                                        pr.competitionname = qb.competitionname AND \
                                            PlayerId = " + playerid + ") IS NULL \
                                THEN 'not saved' \
                                ELSE 'saved' END AS saved \
            FROM QuestionBank qb \
            WHERE qb.competitionname = '" + competitionname + "'"

    #print (sql)
    conn, cur = opendb()

    cur.execute(sql)
    dbrows = cur.fetchall()

    cur.close()
    conn.close()

    return dbrows

def getExpiredCompetitions():
    sql = "SELECT Name FROM competition WHERE datetime('now') > datetime(EndingOn)"

    conn, cur = opendb()

    cur.execute(sql)
    dbrows = cur.fetchall()

    cur.close()
    conn.close()

    return dbrows

def getCompetitionDetail(competionname):
    sql = "SELECT * FROM competition WHERE Name = '" + competionname + "'"
    competionname = ""
    description = ""
    startedon = ""
    endingon = ""
    notes = ""

    rowDict = {}

    conn, cur = opendb()

    cur.execute(sql)
    dbrows = cur.fetchall()

    cur.close()
    conn.close()

    for item in dbrows:
        competionname = dbrows[0][0]
        description = dbrows[0][1]
        startedon = dbrows[0][2]
        endingon = dbrows[0][3]
        notes = dbrows[0][4]
    
        rowDict = {"competitionname": competionname,
                    "description": description,
                    "startedon": startedon,
                    "endingon": endingon,
                    "notes": notes
                    }
    return rowDict

def getQuestionAnwers(competionname):
    sql = "SELECT QId, Quesdesc, ChoiceAnswer FROM QuestionBank WHERE CompetitionName = '" + str(competionname) + "'"
    
    conn, cur = opendb()

    cur.execute(sql)
    dbrows = cur.fetchall()

    cur.close()
    conn.close()

    return dbrows

def isResponded(player_id, qid, competionname):
    conn, cur = opendb()
    
    sql = "SELECT * FROM PlayerResponse WHERE PlayerId = " + player_id + " AND QId = " + qid + " AND competitionname = '" + competionname + "'"

    cur.execute(sql)
    rows = cur.fetchall()
    
    conn.commit()

    cur.close()
    conn.close()

    isresp = False

    if len(rows) > 0:
        isresp = True
    
    return isresp

def registerResponse(player_id, competition_name, qid, qdesc, ans, resptime, points):
    isRegisterOK = True

    try:
        isresp = isResponded(player_id, qid, competition_name)
        data_tuple = ()

        if not isresp:
            sql = "INSERT INTO PlayerResponse (PlayerId, CompetitionName, QId, Question, ResponseChoice, RespondedOn, Points) \
                VALUES (?,?,?,?,?,?,?)"
            data_tuple = (player_id, competition_name, qid, qdesc, ans, str(resptime), points)
        else:
            sql = "UPDATE PlayerResponse \
                SET ResponseChoice = ?, \
                    RespondedOn = ?, \
                    Points = ? \
                WHERE PlayerId = ? AND \
                CompetitionName = ? AND \
                QId = ?"
            data_tuple = (ans, str(resptime), points, player_id, competition_name, qid)

        conn, cur = opendb()

        # print (sql, data_tuple)

        cur.execute(sql, data_tuple)
        rows = cur.fetchall()
        
        conn.commit()

        cur.close()
        conn.close()
    except Exception as ex:
        print ("registerResponse", ex)
        isRegisterOK = False
    
    return isRegisterOK

def getScore(playerid):
    conn,  cur = opendb()
    sql = "SELECT name, pr.CompetitionName, pr.Question, Points, QId FROM PlayerResponse pr, Players p WHERE p.mobile = " + playerid + " AND pr.PlayerId = p.mobile AND pr.SubmittedOn IS NOT NULL ORDER BY pr.competitionname, QId"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def getRanks():
    conn,  cur = opendb()
    sql = "SELECT name, pr.competitionname as competionname, sum(points) as totalpoints, \
        NULL as pointrank,  max(datetime(SubmittedOn)) As submittedon \
        FROM PlayerResponse pr, Players p \
        WHERE pr.PlayerId = p.mobile AND \
            pr.SubmittedOn IS NOT NULL \
        GROUP BY name, pr.competitionname \
        ORDER BY pr.competitionname, sum(Points) DESC, SubmittedOn ASC"

    cur.execute(sql)
    rows = cur.fetchall()
    
    cur.close()
    conn.close()   
    rank_lst = calculateRanks(list(rows))
    # print(rank_lst)
    return rank_lst

def getAccount(playerid):
    conn,  cur = opendb()
    sql = "SELECT name, email, mobile, competitionname FROM Players WHERE mobile = " + str(playerid)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    rowDict = {}

    if len(rows) > 0:
        rowDict = {"playername": rows[0][0],
            "email": rows[0][1],
            "playerid": rows[0][2],
            "competitionname": rows[0][3]
            }
    
    return rowDict

def updateProfile(mobilNo, playername, email, competition):
    isUpdateOK = True

    try:
        sql = "UPDATE Players SET \
                name = '" + playername + "', \
                email = '" + email + "', \
                competitionname = '" + competition + "' \
            WHERE mobile = " + str(mobilNo)
        conn,  cur = opendb()
        cur.execute(sql)
        rows = cur.fetchall()
        
        conn.commit()

        cur.close()
        conn.close()
    except Exception as ex:
        isUpdateOK = False

    return isUpdateOK


def UpdatePassword(mobileNo, npasswd1):
    isUpdateOK = True

    try:
        sql = "UPDATE Players SET \
                password = '" + npasswd1 + "' \
            WHERE mobile = " + str(mobileNo)

        conn,  cur = opendb()
        cur.execute(sql)
        rows = cur.fetchall()
        
        conn.commit()

        cur.close()
        conn.close()
    except Exception as ex:
        print ("UpdatePassword", ex)
        isUpdateOK = False

    return isUpdateOK

def getAnswer(competition_name, qid):
    conn,  cur = opendb()
    sql = "SELECT ChoiceAnswer FROM QuestionBank WHERE Qid = " + str(qid) + " AND CompetitionName = '" + competition_name + "'"
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    rowDict = {}
    answer = ""

    if len(rows) > 0:
        answer = rows[0][0]
    
    return answer

def saveOTP(mobileNo, otpnum, otpvalidtilltime):
    isSaveOK = False
    
    try:            
        conn, cur = opendb()
        
        sql = "INSERT INTO PlayerOtp (PlayerId, OTP, OTPValidTill) \
                    VALUES (?,?,?)"
        
        data_tuple = (mobileNo, otpnum, str(otpvalidtilltime))
            
        cur.execute(sql, data_tuple)
        
        conn.commit()

        cur.close()
        conn.close()

        isSaveOK = True
    except Exception as ex:
        print("saveOTP:", ex)
    
    return isSaveOK

def IsOTPValid(mobileNo, usrotp):
    isOtpOK = False

    try:
        sql = "SELECT OTPValidTill \
                FROM PlayerOtp \
                WHERE PlayerId = " + str(mobileNo) + " AND \
                    OTP = " + str(usrotp) + " AND \
                    datetime(OTPValidTill) >= datetime('now')"

        conn, cur = opendb()

        cur.execute(sql)
        rows = cur.fetchall()
        
        cur.close()
        conn.close()

        if len(rows) > 0:
            isOtpOK = True
    except Exception as ex:
        print("IsOTPValid:", ex)
    
    return isOtpOK

def import_csv_data(csv_file_name, table_name, isHeaderRowPresent=True):
    isImportOK = False

    try:
        # reading csv file 
        with open(csv_file_name, 'r') as csvfile:
            # initializing database
            conn, cur = opendb()
            columnNames = []
            sql = ""

            # creating a csv reader object 
            csvreader = csv.reader(csvfile) 
            
            # extracting field names through first row 
            if isHeaderRowPresent:
                columnNames = next(csvreader) 

            # extracting each data row one by one 
            for row in csvreader:
                sql = "INSERT INTO " + table_name + "(" + ', '.join(column for column in columnNames) + ") \
                            VALUES (" + ', '.join("?" for column in columnNames) + ")"
                
                data_tuple = tuple(row)

                cur.execute(sql, data_tuple)
                    
            conn.commit()

            cur.close()
            conn.close()

            isImportOK = True
    except Exception as e:
        print("csv import error!", e)
    
    return isImportOK