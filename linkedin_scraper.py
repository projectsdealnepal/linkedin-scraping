import requests
from lxml import html

def voyager_api(li_at='', J_SESSION_ID='', company_id=''):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        }

    # company_link = 'https://www.linkedin.com/voyager/api/entities/companies/{}'.format(company_id)
    company_link = 'https://www.linkedin.com/voyager/api/me'
    with requests.session() as s:
        s.cookies['li_at'] = li_at
        s.cookies["JSESSIONID"] = J_SESSION_ID
        s.headers = headers
        s.headers["csrf-token"] = s.cookies["JSESSIONID"].strip('"')
        response = s.get(company_link)
        response_dict = response.json()

        return response_dict


def network_info(li_at='', J_SESSION_ID='', profile_id='ACoAADpSoawBcb0DrAHFo2V4kDUL1rKbeoK6Fnk'):
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    }

    # company_link = 'https://www.linkedin.com/voyager/api/entities/companies/{}'.format(company_id)
    company_link = 'https://www.linkedin.com/voyager/api/identity/profiles/{}/networkinfo'.format(profile_id)
    with requests.session() as s:
        s.cookies['li_at'] = li_at
        s.cookies["JSESSIONID"] = J_SESSION_ID
        s.headers = headers
        s.headers["csrf-token"] = s.cookies["JSESSIONID"].strip('"')
        response = s.get(company_link)
        response_dict = response.json()

        return response_dict

def get_connections(li_at='', J_SESSION_ID=''):
    company_link = 'https://www.linkedin.com/voyager/api/relationships/dash/connections?decorationId=com.linkedin.voyager.dash.deco.web.mynetwork.ConnectionListWithProfile-15&count=40&q=search&sortType=RECENTLY_ADDED'
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    }

    # company_link = 'https://www.linkedin.com/voyager/api/entities/companies/{}'.format(company_id)
    # company_link = 'https://www.linkedin.com/voyager/api/identity/profiles/{}/networkinfo'.format(profile_id)
    with requests.session() as s:
        s.cookies['li_at'] = li_at
        s.cookies["JSESSIONID"] = J_SESSION_ID
        s.headers = headers
        s.headers["csrf-token"] = s.cookies["JSESSIONID"].strip('"')
        response = s.get(company_link)
        response_dict = response.json()

        data = response_dict['elements']
        print(data)
        connections = []
        for d in data:
            connections.append({
                'first_name': d['connectedMemberResolutionResult']['firstName'],
                'last_name': d['connectedMemberResolutionResult']['lastName'],
                'occupation': d['connectedMemberResolutionResult']['headline']
            })
    return connections

def login(username='', password=''):
    URL = 'https://www.linkedin.com/'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
    }
    session = requests.Session()
    response = session.get(URL, headers=headers, timeout=10)
    message = False
    if response.status_code == 200:
        tree = html.fromstring(response.text)
        logincsrf_params = tree.xpath("//input[@name='loginCsrfParam']/@value")
        if logincsrf_params != []:
            login_url = "https://www.linkedin.com/uas/login-submit"
            params = {
                'loginCsrfParam': logincsrf_params[0],
                'session_key': username,
                'session_password': password
            }
            response = session.post(login_url, data=params, timeout=10)
            print(response.cookies.get_dict())
            message = True
    return message



# voyager_api()