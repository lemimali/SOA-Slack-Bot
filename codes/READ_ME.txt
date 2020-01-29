Requests will always run a sequence of functions.
The first function always does the actual work and the second function (slack_informer)
makes and sends information to Slack Bot.

Possible functions are:
GET get_deck		Returns one deck from database. Wants value "deckname" in JSON form.
GET decks		Returns all the decks with basic information.
DELETE delete_deck 	Deletes one deck from database. Wants value "delete" (deck name) in JSON form.
POST add_deck		Creates a new deck to database. Wants "deckname" and "cardurls" array with at least
			one value in it in JSON form. A value in "cardurls" has "url" (MTG card in JSON form
			from Scryfall.com) and "amount" (how many copies of this card you want to add in your deck).

Sequence of update_deck_prices and slack_informer is triggered every six hours in the Cloud.
Slack Bot will inform when updating has succeeded or failed.