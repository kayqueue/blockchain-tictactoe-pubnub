import json, hashlib

from gameboard import start_game, make_a_move, check_turn, win_or_draw

def write_block(player, board, turns_taken):
	# total number of turns taken
	number_of_turns = sum(turns_taken.values())
	
	# check legality of turn
	correct_turn = check_turn(player, turns_taken)
	if not correct_turn:
		return
	
	# verify new block, except for genesis block
	if number_of_turns != 0:
		valid = verify_new_block(number_of_turns)
	
		if not valid:
			exit("Latest block is invalid! Game is stopping...")
	
	# open the latest file
	with open(str(number_of_turns) + ".json", "r") as fin:
		# get hash of previous block
		hash_of_previous_block = hashlib.sha256(fin.read().encode()).hexdigest()
		
		# move file cursor back to the beginning
		fin.seek(0)
		
		# get the TxID of the latest file
		turn_number = json.loads(fin.read())["TxID"]
		
	# generate new block
	nonce = 0
	flag = True
	move = make_a_move(player, board, turns_taken)
	
	# player's name
	if player == "A":
		player = "Alice"
		
	if player == "B":
		player = "Bob"
	
	while(flag):
		new_block = json.dumps({"TxID": turn_number + 1, "Hash": hash_of_previous_block, "Nonce": nonce, "Transaction": [player, move]}, indent = 4)
		hash_new_block = hashlib.sha256(new_block.encode()).hexdigest()
		
		# require the hash to be < 2**244/2**256:
		# (256 - 244) / 4 == 3
		if int(hash_new_block, 16) < int("000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 16):
			flag = False
			
		nonce += 1
	
	# write new block
	with open(str(turn_number + 1) + ".json", "w") as fout:
		fout.write(new_block)
	
	# possibility of winning
	if turn_number + 1 >= 5:
		winner_found = win_or_draw(turn_number + 1, board)

		if turn_number % 2 == 0 and winner_found: # Alice
			exit("Alice won!")
		
		if turn_number % 2 == 1 and winner_found: # Bob
			exit("Bob won!")
		
		if turn_number + 1 == 9 and not winner_found: # Draw
			exit("Game board is full. No more playable moves!\nResult: Draw")
			

##################################

# verify new block
def verify_new_block(block_number):
	with open(str(block_number - 1) + ".json", "r") as fin:
		hash_of_previous_block = hashlib.sha256(fin.read().encode()).hexdigest()
		
	with open(str(block_number) + ".json", "r") as fin:
		hash_of_new_block = json.loads(fin.read())["Hash"]
		
	if hash_of_previous_block == hash_of_new_block:
		return True
	else:
		return False


		
###################################

def main():
	# Start game
	# stores board condition and turns taken by each player as separate dictionaries
	board, turns_taken = start_game()
	
	write_block("A", board, turns_taken)
	write_block("B", board, turns_taken)
	write_block("A", board, turns_taken)
	write_block("B", board, turns_taken)
	write_block("A", board, turns_taken)
	write_block("B", board, turns_taken)
	write_block("A", board, turns_taken)
	write_block("B", board, turns_taken)
	write_block("A", board, turns_taken)

if __name__ == "__main__":
	main()
