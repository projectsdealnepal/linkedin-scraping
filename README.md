# 1. install requirements.txt file
    Run the application in command using
    python main.py
# 2. No database has been used and is just for testing purpose. Later we will implement username and password in database table
    Input username and password in main.py
    app.config['LINKEDIN_USERNAME'] = 'xxx'                               # put your linkedin username
    app.config['LINKEDIN_PASSWORD'] = 'xxx'                           # put your linkedin password
# 3. generate token 
    using url endpoint /api/token
    Basic Authentication is used to generate token
    Input linkedin: username and password to generate a taken.
# 4. After token is generated this token is used to validate every endpoint
    /api/companies/{{company_id}} is used to pull company information
    put the token key in header
    headers = {
    'token': 'TOKEN_KEY'
    }
# 5. Selenium Scrapper
    Selenium scraper has been used to login and then get cookies
    linkedin_selenium.py
    you can either use Firefox, Chrome or Phantom. By default its Firefox.
    Please change the path of driver in Line 11 of linkedin_selenium.py
    input_params = {

            'driver_path': 'C:\chromedriver.exe',
            'firefox_path': 'C:\geckodriver.exe',
            'phantom_path': 'C:\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',
            'url': 'https://www.linkedin.com/',

        }

# 6. Voyager API
    in file linkedin_scraper.py
