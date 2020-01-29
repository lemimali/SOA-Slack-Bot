import sys
from urllib import request, parse
import json

def main(dict):
    
    # Checking if we got an error earlier
    if "error_message" in dict:
        return { "error_message": dict["error_message"] }
    
    # Checking what type of message we are going to build
    msg = None
    try:
        tag = dict["tag"]
        if tag == "add":
            msg = make_add_deck_msg(dict)
        elif tag == "delete":
            msg = make_delete_deck_msg(dict)
        elif tag == "get_deck":
            msg = make_get_deck_msg(dict)
        elif tag == "get_decks":
            msg = make_get_all_decks_msg(dict)
        elif tag == "update":
            msg = make_update_msg(dict)
        else:
            return { "error_message": "Error while trying to check message type! 'tag' value is incorrect." }
    except KeyError:
        return { "error_message": "Error while trying to check message type! 'tag' value is missing." }

    # POST message to Slack Bot
    make_post(msg)
    
    # Returning message to client
    return { 'message': dict["message"] }


# Creates a message that will be sent to Slack Bot after new deck is added.
def make_add_deck_msg(dict):
    return {"text": f":tada::tada:*{dict['message']}*:tada::tada:\n :black_medium_small_square:Deck name: *{dict['deckname']}*\n :black_medium_small_square:Number of cards: *{dict['amount']}*\n :black_medium_small_square:Deck's "
                f"current value according MagicCardMarket: *{dict['value']}€* :euro:"}

# Creates a message that will be sent to Slack Bot after a deck is removed.
def make_delete_deck_msg(dict):
    return {"text": f":x: A deck named *{dict['delete']}* has been removed! :x:"}


# Creates a message including deck's info that will be sent to Slack Bot.
def make_get_deck_msg(dict):
    ret = f"A deck named *{dict['deckname']}* contains the following cards:\n\n"
    
    totalvalue = 0
    for card in dict["cardurls"]:
        info = get_card_info(card["url"])
        ret = ret + f"     *{card['amount']}x*    {info['name']}   _{info['set']}_   *{info['value']}€*\n"
        totalvalue += float(info['value']) * float(card['amount'])
    ret = ret + f"     _Deck's total price:_ *{round(totalvalue, 2)}€* :euro:\n"
    ret = ret + f"\n_Card prices reflect to MagicCardMarket's current Price Trends._"
    return {"text": ret }
    
    
# Function that fetches card data from card's JSON url.
def get_card_info(cardurl):
    response = request.urlopen(cardurl)
    data = json.loads(response.read())
    prices = data["prices"]
    value = prices["eur"]
    name = data["name"]
    set = data["set"]
    return { "name": name, "value": float(value), "set": set.upper() }


# Creates a message including all decks that will be sent to Slack Bot.
def make_get_all_decks_msg(dict):
    ret = f"Deck library contains the following decks:\n\n"
    
    for deck in dict["decks"]:
        ret = ret + f"     :black_small_square:*{deck['name']}* contains *{deck['card_amount']}* cards and has price value of *{deck['value']}€*\n"
    ret = ret + f"\n_Card prices reflect to MagicCardMarket's current Price Trends._"
    return {"text": ret }


# Creates a message informing that deck prices were updated. This will be sent to Slack Bot.
def make_update_msg(dict):
    if (dict["success"]):
        ret = f":alarm_clock:Deck prices were updated automatically at {dict['time']}."
        return {"text": ret}
    ret = f":alarm_clock:Deck price updating failed at {dict['time']}."
    return {"text": ret}


# Creates POST for Slack Bot.
def make_post(msg):
    params = json.dumps(msg).encode('utf-8')
    req = request.Request("https://hooks.slack.com/services/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RZ", data=params,
        headers={'content-type': 'application/json'})
    request.urlopen(req)
    