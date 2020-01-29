import sys
import json
from urllib.request import urlopen
from cloudant.client import Cloudant
from urllib.error import HTTPError
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.document import Document
from datetime import datetime, timedelta

def main(dict):
    
    # Connecting Cloudant client
    serviceUsername = "3e757df4-b583-42a5-9c83-67f2d1bc3d1027-bluemix"
    servicePassword = "bf418420e5965dd5b7cd180dfe3ec6467d9c1a662890c37dfd01a9ad27b518f217"
    serviceURL = "https://3e757df4-b583-42a5-9c83-67f2d1bc3d10-bluemix:bf27418420e5965dd5b7cd180dfe3ec6467d9c1a662890c37dfd01a9adb518f217@3e757df4-b583-42a5-9c83-67f2d1bc3d10-bluemix.cloudantnosqldb.appdomain.cloud"
    client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
    client.connect()
    
    # Fetching JSON-file where decks are written
    databaseName = "deck-database"
    database = client.__getitem__(databaseName)
    deckfile = database.__getitem__("6ce8ea8c29e12ec8ec21e4a45787ad94")
    
    # Looping through decks and updating deck prices.
    try:
        for deck in deckfile["decks"]:
            currentval = 0.0
            for urls in deck["cardurls"]:
                currentval += get_price(urls["url"]) * urls["amount"]
            deck["value"] = round(currentval, 2)
    
        # Saving deckfile and closing client
        deckfile.save()
        client.disconnect()
        
        # Getting time when updating was done
        now = (datetime.now() + timedelta(hours=3)).strftime('%c')
        return { 'message': 'Database updated!', 'time': str(now), 'tag': "update", 'success': True }
    except HTTPError as err:
        client.disconnect()
        now = (datetime.now() + timedelta(hours=3)).strftime('%c')
        return { 'message': 'Database updating failed!', 'time': str(now), 'tag': "update", 'success': False }
    
    
# Function that fetches the current value of the card.
def get_price(cardurl):
    response = urlopen(cardurl)
    data = json.loads(response.read())
    prices = data["prices"]
    value = prices["eur"]
    return float(value)
