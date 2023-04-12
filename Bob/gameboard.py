import random, json

# print out the state of the game board
def print_board(board):
	print(f" {board['A']} | {board['B']} | {board['C']} ")
	print("---+---+---")
	print(f" {board['D']} | {board['E']} | {board['F']} ")
	print("---+---+---")
	print(f" {board['G']} | {board['H']} | {board['I']} ")
	print("\n")
	
############################################################

# player makes a move
def make_a_move(player, txid):
	player = player[0] 

	position_is_not_filled = True #  make a move on an empty space
	
	with open("board.json", "r") as fin:
		board = json.loads(fin.read())
			
	# check whether space is empty
	while(position_is_not_filled):
		# generate random letter for move to be played
		move = chr(random.randint(ord('A'), ord('I')))	
		
		if board[move] == " ": # position to be played is empty
			print(f"Turn {txid} - Player {player} played position {move}:")
			print("------------------------------------")
			board[move] = player.upper() # execute move
			
			position_is_not_filled = False # exit while loop
			
			print_board(board) # print state of board after move
			
			return move
		else: # if space is not empty, pick another spot randomly again
			continue			

############################################################

# check for winning combinations
def winning_combination(player_played):
	# winning combinations
	win_con = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"], ["A", "D", "G"], ["B", "E", "H"], ["C", "F", "I"], ["A", "E", "I"], ["C", "E", "G"]]
	
	for i in win_con:
		# check whether player has played the winning move
		check = all(item in player_played for item in i)
		
		# if winning combination is found, return True
		if check:
			return True
	
	return False

##################################

# check for winning condition
def win_or_draw(turn_number, board):	
	# AFTER player makes a move, 2 conditions have to be checked
	# FIRST CONDITION --> Winner is found
	# list of moves each player has made
	alice_played = [i for i in board if board[i] == "A"]
	bob_played = [i for i in board if board[i] == "B"]
	# check for Alice winning condition after her move
	if turn_number % 2 != 0:
		win = winning_combination(alice_played)
		if win:
			return True
	else: # check for Bob winning condition after his move
		win = winning_combination(bob_played)
		if win:
			return True
	# SECOND CONDITION --> Board is full				
	# if no winner is found after board has been filled, end game in draw
	if turn_number == 9:
		return False
		
	return False
