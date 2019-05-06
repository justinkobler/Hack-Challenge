import json
from db import db, Teams, Away, Home, User
from flask import Flask, request
import users_dao

app = Flask(__name__)

db_filename = 'auth.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

def extract_token(request):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        return False, json.dumps({'error' : 'Missing authorization header.'})

    bearer_token = auth_header.replace('Bearer ', '').strip()
    if not bearer_token:
        return False, json.dumps({'error' : 'Invalid authorization header.'})
    return True, bearer_token


@app.route('/register/', methods=['POST'])
def register_account():
    post_body = json.loads(request.data)
    email = post_body.get('email')
    password = post_body.get('password')

    if email is None or password is None:
        return json.dumps({'error' : 'Invalid email or password'})

    created, user = users_dao.create_user(email,password)
    if not created:
        return json.dumps({'error' : 'User already exists'})
    return json.dumps({
        'session_token' : user.session_token,
        'session_expiration' : str(user.session_expiration),
        'update_token' : user.update_token
    })

@app.route('/login/', methods=['POST'])
def login():
        post_body = json.loads(request.data)
        email = post_body.get('email')
        password = post_body.get('password')

        if email is None or password is None:
            return json.dumps({'error' : 'Invalid email or password'})

        success, user = users_dao.verify_credentials(email, password)
        if not success:
            return json.dumps({'error': 'Incorrect email or password'})

        return json.dumps({
            'session_token' : user.session_token,
            'session_expiration' : str(user.session_expiration),
            'update_token' : user.update_token
        })

@app.route('/session/', methods=['POST'])
def update_session():
    success, update_token = extract_token(request)
    if not success:
        return update_token

    try:
        user = users_dao.renew_session(update_token)
    except:
        return json.dumps({'error': 'Invalid update token'})

    return json.dumps({
        'session_token' : user.session_token,
        'session_expiration' : str(user.session_expiration),
        'update_token' : user.update_token
    })

@app.route('/secret/', methods=['GET'])
def secret_message():
    success, session_token = extract_token(request)

    if not success:
        return session_token

    user = users_dao.get_user_by_session_token(session_token)
    if not user or not user.verify_session_token(session_token):
        return json.dumps({'error' : 'Invalid session token'})
    return json.dumps({'messsage' : 'Logged in as ' + user.email})

# Creates a user
@app.route('/api/users/', methods =['POST'])
def create_user():
    post_body = json.loads(request.data)
    user = User(
        teams = post_body.get('teams'),
        username = post_body.get('username')
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success' : True, 'data' : user.serialize()}), 201

# Get a specific team
@app.route('/api/teams/<int:team_id>/', methods = ['GET'])
def get_team(team_id):
    team = Teams.query.filter_by(id=team_id).first()
    if team is None:
        return json.dumps({'success':False,'error': 'Team Not Found'}), 404
    return json.dumps({'success':True,'data':team.serialize()}), 200

# Creates a team
@app.route('/api/teams/', methods = ['POST'])
def create_team():
    post_body = json.loads(request.data)
    created_team = Teams(
        name = post_body.get('name')
    )
    db.session.add(created_team)
    db.session.commit()
    return json.dumps({'success':True, 'data':created_team.serialize()}), 201

# Adds a team to a specific user
@app.route('/api/users_team/<int:user_id>/', methods = ['POST'])
def add_team_to_user(user_id):
    specific_user = User.query.filter_by(id=user_id).first()
    if specific_user is not None:
        post_body = json.loads(request.data)
        team = Teams(
            name = post_body.get('name')
        )
        specific_user.teams.append(team)
        db.session.add(team)
        db.session.commit()
        return json.dumps({'success':True,'data':specific_user.serialize()}), 200
    return json.dumps({'success':False,'error':'User Not Found'}), 404


# Deleting a specific team that the user doesn't want on their favorites anymore
@app.route('/api/teams/<int:team_id>/', methods = ['DELETE'])
def delete_team(team_id):
    specific_team = Teams.query.filter_by(id=team_id).first()
    if specific_team is not None:
        db.session.delete(specific_team)
        db.session.commit()
        return json.dumps({'success':'True', 'data': specific_team.serialize()}), 200
    return json.dumps({'success': 'False', 'error' : 'Team Not Found'}), 404

# Get score for Home team
@app.route('/api/home/<int:home_id>/', methods = ['GET'])
def home_score(home_id):
    score = Home.query.filter_by(id=home_id).first()
    if score is None:
        return json.dumps({'success':False, 'error':'Score Not Found'}), 404
    return json.dumps({'success': True, 'data' : score.serialize()}), 200

# Get score for away team
@app.route('/api/away/<int:away_id>/', methods = ['GET'])
def away_score(away_id):
    score = Away.query.filter_by(id=away_id).first()
    if score is None:
        return json.dumps({'success':False, 'error' : 'Score Not Found'}), 404
    return json.dumps({'success':True, 'data' : score.serialize()}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
