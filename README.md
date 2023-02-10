
# FlaskSalesforceOAuth
Flask + Salesforce Connected App + Simple Salesforce.
This code is an end to end OAuth authentication based on [Salesforce-Oauth2-REST-Metadata-API-Python-Examples](https://github.com/jctissier/Salesforce-Oauth2-REST-Metadata-API-Python-Examples) 

This code is only for "quick and dirty" proof-of-concept purposes, and not a production code.

## Prerequisites 
1. Get a domain name and a server; clone the repo and install the requirements 
2. Create a Salesforce developer account; Follow instructions [here](https://webkul.com/blog/create-free-developer-account-in-salesforce/)
3. Create a Salesforce connected app; Follow instructions [here](https://soft-builder.com/how-to-create-a-connected-app-salesforce/); The redirect URL should be "https://YOURDOMAIN.com:7000/sfdemo/sfsuccess"  
4. Obtain the app's consumer key; Go to App Manager → Edit → Save → Manage Consumer Details
5. Salesforce will only redirect back to a https url; Generate certificate using [certbot](https://certbot.eff.org/)

## Configuration 

    # Salesforce Connected App:  
    REDIRECT_LINK = "https://YOURDOMAIN.com:7000/sfdemo/sfsuccess"  
    CUSTOMER_KEY = "YOUR_CUSTOMER_KEY"  
      
    # Flask SSL configuration  
    PRIVATE_KEY_PATH = '/etc/letsencrypt/live/DOMAIN.COM/privkey.pem'  
    CERTIFICATE_PATH = '/etc/letsencrypt/live/DOMAIN.COM/cert.pem'

## Licence
MIT License
