from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

# my python files
from gameboard import win_or_draw, print_board
from process_message import verify_new_block, update_board

import json

pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-1a59051c-8e51-4b09-862f-f11d66db046b'
pnconfig.publish_key = 'pub-c-13335977-1e4f-468c-a9c3-d7051ed63c76'
pnconfig.user_id = "Bob"
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
	# Check whether request successfully completed or not
	if not status.is_error():
		pass  # Message successfully published to specified channel.
	else:
		pass  # Handle message publish error. Check 'category' property to find out possible issue
			# because of which request did fail.
			# Request can be resent using: [status retry];

class MySubscribeCallback(SubscribeCallback):
	def presence(self, pubnub, presence):
		pass  # handle incoming presence data

	def status(self, pubnub, status):
		if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
			pass  # This event happens when radio / connectivity is lost

		elif status.category == PNStatusCategory.PNConnectedCategory:
			# Connect event. You can do stuff like publish, and know you'll get it.
			# Or just use the connected event to confirm you are subscribed for
			# UI / internal notifications, etc
			pubnub.publish().channel('Channel-mzonikory').message(f'{pnconfig.user_id} has joined the game.').pn_async(my_publish_callback)
		elif status.category == PNStatusCategory.PNReconnectedCategory:
			pass
			# Happens as part of our regular operation. This event happens when
			# radio / connectivity is lost, then regained.
		elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
			pass
			# Handle message decryption error. Probably client configured to
			# encrypt messages and on live data feed it received plain text.

	
	def message(self, pubnub, message):
		# Handle new message stored in message.message
		print(message.message)
        
		# save subscribe message in a file
		with open("subscribe_message.txt", "a") as fout:
			fout.write(str(message.message))
			fout.write("\n")
		
		# count number of lines in the text file
		with open("subscribe_message.txt", "r") as fin:
			for count, line in enumerate(fin):
				pass

		total_lines = count + 1

		# create a game board -- game started
		if total_lines == 1:
			# creates a game board using a dictionary to track its state
			board = json.dumps({"A": " ", "B": " ", "C": " ", "D": " ", "E": " ", "F": " ", "G": " ", "H": " ", "I": " "})
			with open("board.json", "w") as fout:
				fout.write(board)
				
			# get the genesis block
			with open("../0.json", "r") as fin:
				genesis_block = json.loads(fin.read())
			
			with open("0.json", "w") as fout:
				fout.write(json.dumps(genesis_block, indent = 4))

		if total_lines > 1:
			number_of_blocks_written = int((total_lines - 1) / 9)

			# stores the new block in a json file
			with open("subscribe_message.txt", "r") as fin:
				next(fin) # skips the first line of message - "Bob has joined the game"
				
				# skip irrelevant lines
				for i in range((number_of_blocks_written - 1) * 9):
					next(fin)
				
				# store new block
				with open(str(number_of_blocks_written) + ".json", "a") as fout:
					temp = json.loads(fin.read())
					fout.write(json.dumps(temp, indent = 4))
						
			# verify new block
			valid = verify_new_block(number_of_blocks_written)
			
			if not valid:
				exit("Last block is invalid")
						
			# get the move played by the opponent			
			board, player, move = update_board(str(number_of_blocks_written) + ".json")
			
			# print the current state of the game board
			print(f"Turn {number_of_blocks_written} - Player {player[0]} played position {move}:")
			print("------------------------------------")			
			print_board(board)
				
			# verify win_con
			if number_of_blocks_written >= 5:
				winner_found = win_or_draw(number_of_blocks_written, board)
				
				if winner_found:
					print(f"{player} has won the match!")
					pubnub.unsubscribe().channels("Channel-mzonikory").execute()
				
				if not winner_found and number_of_blocks_written == 9: # Draw
					print("Game board is full. No more playable moves!\nResult: Draw")				
					pubnub.unsubscribe().channels("Channel-mzonikory").execute()

pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('Channel-mzonikory').execute()
