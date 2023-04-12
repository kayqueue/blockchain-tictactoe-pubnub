import random

from genesis_block import genesis_block

# start the game
def start_game():
	# create genesis_block
	genesis_block()

	# creates a game board using a dictionary to track its state
	board = {"A": " ", "B": " ", "C": " ", "D": " ", "E": " ", "F": " ", "G": " ", "H": " ", "I": " "}
	
	print("Game has started!")
	print("-----------------")
	
	# prints out state of the game board
	print_board(board)
	
	# to keep track of the turns taken by each player
	turns_taken = {"A": 0, "B": 0}
	
	return board, turns_taken

############################################################

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
def make_a_move(player, board, turns_taken) -> dict:
	player = player.upper() # convert to uppercase

	position_is_not_filled = True #  make a move on an empty space
	
	# check whether space is empty
	while(position_is_not_filled):
		# generate random letter for move to be played
		move = chr(random.randint(ord('A'), ord('I')))	
		
		if board[move] == " ": # position to be played is empty
			print(f"Turn {sum(turns_taken.values()) + 1} - Player {player} played position {move}:")
			print("------------------------------------")
			board[move.upper()] = player.upper() # execute move
			
			position_is_not_filled = False # exit while loop
			
			print_board(board) # print state of board after move
		
			turns_taken[player] += 1 # update turn taken
		else: # if space is not empty, pick another spot randomly again
			continue	
	return move			

############################################################

# check for legality of turn		
def check_turn(player, turns_taken):
	# It is Alice's turn if the number of moves made by Alice is equal to Bob's
	if player == "A":
		if turns_taken["A"] == turns_taken["B"]:
			return True
		else:
			print(f"It is not your turn yet Player {player}")
			return False
	else: # It is Bob's turn if the number of moves made by Bob is 1 less than Alice's
		if turns_taken["A"] - turns_taken["B"] == 1:
			return True
		else:
			print(f"It is not your turn yet Player {player}")			
			return False

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
	winner_found = False
	
	if turn_number >= 5: # Alice has made her third move (possible winning combination)
		# list of moves each player has made
		alice_played = [i for i in board if board[i] == "A"]
		bob_played = [i for i in board if board[i] == "B"]
		# check for Alice winning condition after her move
		if turn_number % 2 != 0:
			win = winning_combination(alice_played)
			if win:
				winner_found = True
				return winner_found
		else: # check for Bob winning condition after his move
			win = winning_combination(bob_played)
			if win:
				winner_found = True
				return winner_found
	# SECOND CONDITION --> Board is full				
	# if no winner is found after board has been filled, end game in draw
	if turn_number == 9:
		return False
