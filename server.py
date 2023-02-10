import sys
from flask import Flask, redirect, url_for, json, session, request
from flask_cors import CORS
import urllib.parse as urlparse
from simple_salesforce import Salesforce
from salesforce_user_agent_flow import SalesforceOAuth2
from OpenSSL import SSL

# Configuration:

# Salesforce Connected App:
REDIRECT_LINK = "https://YOURDOMAIN.com:7000/sfdemo/sfsuccess"
CUSTOMER_KEY = "YOUR_CUSTOMER_KEY"

# Flask SSL configuration
PRIVATE_KEY_PATH = '/etc/letsencrypt/live/DOMAIN.COM/privkey.pem'
CERTIFICATE_PATH = '/etc/letsencrypt/live/DOMAIN.COM/cert.pem'

#####
FLASK_SECRET_KEY = "RANDOM STRING"
SERVER_PORT = 7000
SERVER_HOST = "0.0.0.0"
#################################################

instance_url = None
access_token = None

flask_app = Flask(__name__)
flask_app.secret_key = FLASK_SECRET_KEY

CORS(flask_app)
oauth = SalesforceOAuth2(
    client_id=CUSTOMER_KEY,
    redirect_uri=REDIRECT_LINK,
    sandbox=False
)

@flask_app.route('/')
def index():
    return f"""
    <html>
     <head>
       <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
     </head>
     <body align="center"> 
     <h1>Connect Salesforce to Nominal</html>
    <div style="margin:40px">
    <button type="button" class="btn btn-primary" onclick="location.href='/redir';"> Connect to Salesforce</button>
    </div>
    </body>
    </html>
    """


@flask_app.route("/redir")
def redir():
    """
    The OAuth API will generate a redirect client code to allow the user to authorize the app in Salesforce's
    portal.
    """
    sf_authentication = oauth.get_access_token()
    return sf_authentication.text


@flask_app.route("/sfdemo/token")
def token():
    return session["access_token"]


@flask_app.route("/sfdemo/contact")
def contract():
    sf = Salesforce(instance_url=session["instance_url"], session_id=session["access_token"])
    data = sf.query_all_iter("SELECT COUNT(Id) FROM Contact")
    return json.dumps(next(data)["expr0"])


@flask_app.route("/sfdemo/opportunity")
def opportunities():
    sf = Salesforce(instance_url=session["instance_url"], session_id=session["access_token"])
    data = sf.query_all_iter("SELECT COUNT(Id) FROM Opportunity")
    return json.dumps(next(data)["expr0"])


@flask_app.route("/sfdemo/connected")
def connected():
    return """
    <html>
     <head>
       <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
     </head>
     <body align="center"> 
     <h1>Connected Successfully</html>
     <script>

     async function fetchUrl
     (url) {
            let response = await fetch(url);
            let data = await response.text();
            document.getElementById('content').innerHTML=data;
        }
     </script>
     
    <div style="margin:40px">
            <button type="button" class="btn btn-info" onclick="fetchUrl('./token')">Access Token</button>
            <button type="button" class="btn btn-info" onclick="fetchUrl('./contact')">#Contacts</button>
            <button type="button" class="btn btn-info" onclick="fetchUrl('./opportunity')">#opportunities</button>
    </div>
    
    <div id="content" class="alert alert-success" role="alert">
    </div>
    </body>
    </html>
    """

@flask_app.route("/sfdemo/sfsuccess")
def success():
    """
    When the App is authorized by Salesforce, the user's browser is redirected back to the server. The token code
    is the fragment ("#") part of the URL which is not visible to the server.
    This code converts the fragment to query parameters, so the server can perform SOQL queries.
    """
    return """
     <html>
     <head>
        <script>
            var hash = window.location.hash.substring(1)
            window.location.href = "./savetokens" + "?" + hash
        </script>
     </head>
     </html>
    
    """


@flask_app.route("/sfdemo/savetokens")
def savetokens():
    session["instance_url"] = request.args.get("instance_url")
    session["access_token"] = request.args.get("access_token")
    return redirect(url_for('connected'))


if __name__ == '__main__':
    context = (CERTIFICATE_PATH, PRIVATE_KEY_PATH)
    flask_app.run(host=SERVER_HOST, port=SERVER_PORT, debug=True, ssl_context=context)
