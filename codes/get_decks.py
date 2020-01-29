import sys
import json
from urllib.request import urlopen
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.document import Document

def main(dict):
    
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
    
    # Creating data that will be sent back to client
    data = {}
    data["decks"] = []
    for deck in deckfile["decks"]:
        deckdata = {}
        deckdata["name"] = deck["deckname"]
        deckdata["value"] = deck["value"]
        deckdata["card_amount"] = deck["card_amount"]
        data["decks"].append(deckdata)
    data["tag"] = "get_decks"
    data["message"] = "Decks are presented in Slack by MTG Deck Bot."
    
    client.disconnect()
    
    return data
