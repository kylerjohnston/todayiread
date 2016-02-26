from flask_restful import Resource, abort
from ..models import User

def get_user(username):
    user = User.query.filter_by(username = username).first()
    if user is not None:
        return user
    else:
        abort(404, message = 'User {} does not exist'.format(username))

def jsonify_sessions(session_list):
    session_dict_list = {}
    session_dict_list['session'] = []
    for session in session_list:
        this_session = {
            'title': session.title.title,
            'author': session.title.author,
            'genre': session.title.genre,
            'pages': session.pp,
            'date': session.date.strftime('%Y %m %d')
        }
        session_dict_list['session'].append(this_session)

    return session_dict_list

def get_all_sessions(username):
    user = get_user(username)
    all_sessions = user.sessions.all()
    return jsonify_sessions(all_sessions)

class SessionList(Resource):
    def get(self, username):
        return get_all_sessions(username)
