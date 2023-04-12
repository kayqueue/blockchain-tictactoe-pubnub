from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from gameboard import make_a_move
import hashlib, json


pnconfig = PNConfiguration()

pnconfig.subscribe_key = 'sub-c-1a59051c-8e51-4b09-862f-f11d66db046b'
pnconfig.publish_key = 'pub-c-13335977-1e4f-468c-a9c3-d7051ed63c76'
pnconfig.user_id = "Alice"
pubnub = PubNub(pnconfig)


def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];

def send_message(block):
	pubnub.publish().channel("Channel-mzonikory").message(block).pn_async(my_publish_callback)

def write_block():
	with open("subscribe_message.txt", "r") as fin:
		for count, line in enumerate(fin):
			pass
	total_lines = count + 1
	
	if total_lines == 1:
		exit("Bob has not joined yet!")
	
	# no blocks yet - except genesis block
	if total_lines - 2 == 0:
		with open("../0.json", "r") as genesis_block:
			# hash of genesis block
			hash_of_previous_block = hashlib.sha256(genesis_block.read().encode()).hexdigest()
			
			genesis_block.seek(0) # move cursor back to start of file
			
			# TxID of genesis block
			txid = json.loads(genesis_block.read())["TxID"] + 1
	else:
		number_of_blocks = int((total_lines - 2) / 9)
			
		# open latest block	
		with open(str(number_of_blocks) + ".json", "r") as fin:
			# hash of previous block
			hash_of_previous_block = hashlib.sha256(fin.read().encode()).hexdigest()
			
			fin.seek(0) # move cursor back to start of file
			
			# TxID of genesis block
			txid = json.loads(fin.read())["TxID"] + 1
			
	# check turn order
	if txid % 2 == 0:
		print(f"It is not your turn yet {pnconfig.user_id}")
		return
		
	# generate new block
	nonce = 0
	flag = True
	move = make_a_move(pnconfig.user_id, txid)
	
	while(flag):
		block = json.dumps({"TxID": txid, "Hash": hash_of_previous_block, "Nonce": nonce, "Transaction": [pnconfig.user_id, move]}, indent = 4)
		hash_block = hashlib.sha256(block.encode()).hexdigest()
		
		# require the hash to be < 2**244/2**256:
		# (256 - 244) / 4 == 3
		if int(hash_block, 16) < int("000fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 16):
			flag = False
			send_message(block)
			
		nonce += 1
			


write_block()
