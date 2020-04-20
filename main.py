from controllers import login, home, registration, quiz, leaderboard, account, about, competition
from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = "mysecretkeyforquizapp"
app.config["SESSION_TYPE"] = "filesystem"

sess = Session()
sess.init_app(app)

app.add_url_rule('/', view_func=home.home)
app.add_url_rule('/competitions', view_func=competition.competitions, methods=['GET'])
app.add_url_rule('/competitionanswers', view_func=competition.competitionanswers, methods=['POST'])

app.add_url_rule('/about', view_func=about.about)

app.add_url_rule('/login', view_func=login.login, methods=['GET', 'POST'])
app.add_url_rule('/chklogin', view_func=login.chklogin, methods=['GET', 'POST'])
app.add_url_rule('/forgotpass', view_func=login.forgotpass, methods=['GET'])
app.add_url_rule('/genotp', view_func=login.genotp, methods=['POST'])

app.add_url_rule("/signup", view_func=registration.signup, methods=['GET', 'POST'])
app.add_url_rule('/register', view_func=registration.register, methods=['POST'])
app.add_url_rule('/genpass', view_func=registration.genpass)
app.add_url_rule('/newpassupdate', view_func=registration.newpassupdate, methods=['POST'])

app.add_url_rule('/question', view_func=quiz.question, methods=['GET'])
app.add_url_rule('/submit', view_func=quiz.submit, methods=['POST'])
app.add_url_rule('/questions/<qno>', view_func=quiz.thisQuestion, methods=['GET', 'POST'])
app.add_url_rule('/answersave', view_func=quiz.answersave, methods=['POST'])

app.add_url_rule('/leaderboard', view_func=leaderboard.leaderboard)
app.add_url_rule('/ranks', view_func=leaderboard.ranks)

app.add_url_rule('/account', view_func=account.account, methods=['GET'])
app.add_url_rule('/account', view_func=account.updateaccount, methods=['POST'])
app.add_url_rule('/account/resetpass', view_func=account.resetpassword, methods=['GET'])
app.add_url_rule('/account/resetpass', view_func=account.updatepassword, methods=['POST'])

port = int(os.getenv('PORT', 5000))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=True, host='0.0.0.0', port=port)