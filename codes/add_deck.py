import sys
import json
from urllib.request import urlopen
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from cloudant.document import Document


# Function that fetches the current value of the card.
def get_price(cardurl):
    response = urlopen(cardurl)
    data = json.loads(response.read())
    prices = data["prices"]
    value = prices["eur"]
    return float(value)
    

# Checks if new deck's deck name is already in use.
def deck_name_valid(deckname, decks):
    for deck in decks["decks"]:
        if deckname == deck["deckname"]:
            return False
    return True


def main(dict):
    
    # Checking if new deck has right values in it
    if not "deckname" in dict:
        return { "error_message": "A deck must have a name value ('deckname')" }
    if not "cardurls" in dict:
        return { "error_message": "A deck must have atleast one card (in 'cardurls'). A card must have values 'url' and 'amount'." }
    
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
    
    # Checking if deckname is already in use
    if not deck_name_valid(dict["deckname"], deckfile):
        client.disconnect()
        return { "error_message": "Deck name is already in use." }
    
    # Getting value for the new deck
    currentval = 0.0
    amount_of_cards = 0
    for url in dict["cardurls"]:
        currentval += get_price(url["url"]) * url["amount"]
        amount_of_cards += url["amount"]
    dict["value"] = round(currentval, 2)
    dict["card_amount"] = amount_of_cards
    
    # Removing unnecassary stuff from dict
    if "__ow_headers" in dict:
        dict.pop("__ow_headers");
    if "__ow_method" in dict:
        dict.pop("__ow_method");
    if "__ow_path" in dict:
        dict.pop("__ow_path");
    
    # Adding new deck to the collection
    deckfile["decks"].append(dict)
    deckfile.save()
    
    # Disconnecting from client
    client.disconnect()
    
    # Informing user that adding succeeded
    return { 'message': "A new deck was added succesfully!", 'deckname': dict["deckname"], 'amount': amount_of_cards, 'value': dict["value"], 'tag': "add"}
