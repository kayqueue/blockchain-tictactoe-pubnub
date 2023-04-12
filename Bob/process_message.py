import json, hashlib

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
			
# read a file and return player and move played
def read_file(filename):
	with open(filename, "r") as fin:
		transaction = json.loads(fin.read())["Transaction"]
		player = transaction[0]
		move = transaction[1]
		
	return player, move

# update the state of the board
def update_board(filename):
	player, move = read_file(filename)
	with open("board.json", "r") as fin:
		board = json.loads(fin.read())
		
	with open("board.json", "w") as fout:
		board[move] = player[0]
		fout.write(json.dumps(board))
		
	with open("board.json", "r") as fin:
		return json.loads(fin.read()), player, move
