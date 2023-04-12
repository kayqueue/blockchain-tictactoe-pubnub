Grade: 98/100

# Goal:
Create a simple blockchain system to enable two parties to play a tic-tac-toe game using PubNub package

[1] Generate the genesis block
[2] At each turn, the player who is taking the turn creates a new block in JSON format and sends it to the other player in the following format:
    {
        “TxID": <TxID>,
        "Hash": <Hash>,
        "Nonce": <Nonce>,
        "Transaction": <Transaction>
    }
    TxID: <TxID> of last block + 1
    Hash: SHA256 hash value of last block
    Nonce: SHA256(<current block>) < 2^244
    Transaction: the choice of the player in their turn e.g. ["Alice", B] - B refers to the location in the tic-tac-toe board (program selects a random spot during each turn)
[3] The game continues till all the spaces in the board are taken, or whenever a winner is found, whichever comes first.
[4]

# Recreating the game:
- To recreate the game using pubnub, please refer to recreate-game.txt


# Offline implementation:
- In order to better illustrate the workings of the tic-tac-toe game, I have included a folder 'Offline_Implementation' which includes the program necessary to implement one tic-tac-toe game per execution.
- To recreate the game offline, please refer to offline.txt