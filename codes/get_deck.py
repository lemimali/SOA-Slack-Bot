import sys
import json
from urllib.request import urlopen
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.document import Document

def main(dict):
    
    # Checking if user has typed a deck that this function is trying to find
    if not "deckname" in dict:
        return { "error_message": "Type value to 'deckname' to fetch specific deck's information." }
    
    # Connecting Cloudant client
    serviceUsername = "3e757df4-b583-42a5-9c83-67f2d1bc3d1027-bluemix"
    servicePassword = "bf418420e5965dd5b7cd180dfe3ec6467d9c1a662890c37d27fd01a9adb518f217"
    serviceURL = "https://3e757df4-b583-42a5-9c83-67f2d1bc3d10-bluemix:bf27418420e5965dd5b7cd180dfe3ec6467d9c1a662890c37dfd01a9adb518f217@3e757df4-b583-42a5-9c83-67f2d1bc3d10-bluemix.cloudantnosqldb.appdomain.cloud"
    client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
    client.connect()
    
    # Fetching JSON-file where decks are written
    databaseName = "deck-database"
    database = client.__getitem__(databaseName)
    deckfile = database.__getitem__("6ce8ea8c29e12ec8ec21e4a45787ad94")
    
    # Trying to find deck from database
    name_to_find = dict["deckname"]
    result = {}
    for deck in deckfile["decks"]:
        if name_to_find == deck["deckname"]:
            result = deck
            break
    else:
        return { "error_message": f"Couldn't find a deck named {name_to_find}." }
    
    client.disconnect()
    result["tag"] = "get_deck"
    result["message"] = "Deck's information is presented in Slack by MTG Deck Bot!"
    return result
