import json

def genesis_block():
	genesis_block = json.dumps({"TxID": 0, "Hash": "This is the genesis block.", "Nonce": 0, "Transaction": []}, indent = 4)
	
	# write to 0.json
	with open("0.json", "w") as fout:
		fout.write(genesis_block)
		
genesis_block()
