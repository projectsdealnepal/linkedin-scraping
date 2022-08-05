from flask import Flask, jsonify, request, session
from itsdangerous.serializer import Serializer
from itsdangerous import BadSignature, SignatureExpired
from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from functools import wraps
import jwt
import linkedin_scraper
import linkedin_selenium
import re
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'                                                        # secret key
app.config['LINKEDIN_USERNAME'] = config.username                           # put your linkedin username
app.config['LINKEDIN_PASSWORD'] = config.password                                         # put your linkedin password
app.config['ID'] = 1

# This is just for testing so we have not used the Database, later we will store username and password
# of linkedin in database and call accordingly

# Decorator for Token
# session['li_at'] = None
# session['jsessionid'] = None

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data.get('public_id')
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


# api to extract companies from voyager API

@app.route('/api/companies/<id>', methods=['POST'])
@token_required
def get_company(current_user, id):
    if current_user == app.config['ID']:
        username = app.config.get('LINKEDIN_USERNAME')
        password = app.config.get('LINKEDIN_PASSWORD')
        '''
        write the scraping program here
        '''

        if not 'li_at' in session:
            linkedin = linkedin_selenium.LinkedLn_Scrapper()
            linkedin_cookies = linkedin.login(email1=username, password=password)
            li_at = linkedin_cookies.get('li_at')
            jsession_id = re.sub(r'\"', '', linkedin_cookies.get('JSESSIONID'))
            session['li_at'] = li_at
            session['jsessionid'] = jsession_id
        else:
            li_at = session.get('li_at')
            jsession_id = session.get('jsessionid')

        if li_at != '':
            response = linkedin_scraper.voyager_api(company_id=id, li_at=li_at,
                                                    J_SESSION_ID=jsession_id)
            return jsonify({
                'data': response
            })
        else:
            return make_response('Unable to Login', 401)
    else:
        return make_response('Could not verify', 401)


@app.route('/api/connections', methods=['POST'])
@token_required
def get_network_info(current_user):
    if current_user == app.config['ID']:
        username = app.config.get('LINKEDIN_USERNAME')
        password = app.config.get('LINKEDIN_PASSWORD')
        '''
        write the scraping program here
        '''
        print(session.keys())
        if not 'li_at' in session:
            linkedin = linkedin_selenium.LinkedLn_Scrapper()
            linkedin_cookies = linkedin.login(email1=username, password=password)
            li_at = linkedin_cookies.get('li_at')
            jsession_id = re.sub(r'\"', '', linkedin_cookies.get('JSESSIONID'))
            session['li_at'] = li_at
            session['jsessionid'] = jsession_id
        else:
            li_at = session.get('li_at')
            jsession_id = session.get('jsessionid')

        if li_at != '':
            response = linkedin_scraper.get_connections(li_at=li_at,
                                                    J_SESSION_ID=jsession_id)
            return jsonify({
                'data': response
            })
        else:
            return make_response('Unable to Login', 401)
    else:
        return make_response('Could not verify', 401)
# generates the token key

@app.route('/api/token', methods=['POST'])
def generate_token():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    # user = Users.query.filter_by(name=auth.username).first()
    # print(check_password_hash(app.config['PASSWORD'], auth.password))
    if (app.config['LINKEDIN_PASSWORD'] == auth.password):
        token = jwt.encode(
            {'public_id': app.config['ID'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
            app.config['SECRET_KEY'], "HS256")

        return jsonify({'token': token})

    return make_response('could not verify', 401, {'Authentication': '"login required"'})


if __name__ == '__main__':
    app.run(debug=True)
