'''
from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify
import atexit
import os
import json

app = Flask(__name__, static_url_path='')

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif "CLOUDANT_URL" in os.environ:
    client = Cloudant(os.environ['CLOUDANT_USERNAME'], os.environ['CLOUDANT_PASSWORD'], url=os.environ['CLOUDANT_URL'], connect=True)
    db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On IBM Cloud Cloud Foundry, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def root():
    return app.send_static_file('index.html')

# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    data = {'name':user}
    if client:
        my_document = db.create_document(data)
        data['_id'] = my_document['_id']
        return jsonify(data)
    else:
        print('No database')
        return jsonify(data)

@atexit.register
def shutdown():
    if client:
        client.disconnect()
'''

from controllers import login, home, registration, quiz, leaderboard, account, about, competition, admin
from flask import Flask, session
from flask_session import Session
import os
from common import config

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

app.add_url_rule('/admin', view_func=admin.admin, methods=['GET', 'POST'])

port = int(os.getenv('PORT', 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)
