#module 1 Create a blockchain
import datetime # to find the exact date 
import hashlib #hash the block
import json # encode the blocks
from flask import Flask, jsonify 


building a blockchain
class Blockchain:
    def __init__(self):
        self.chain= [] #initialzation of block
        self.create_block(proof = 1, previous_hash ='0' )# Genesis block 
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1, # dictionary
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof, # consensus
                 'previous_hash': previous_hash} # to link the blockchain
        self.chain.append(block)
        return block
    
    def get_prev_block(self):
        return self.chain[-1] #index of previous block
    # proof of work
    
    def proof_of_work(self, previous_proof):
        new_proof = 1 # increment after each iteration till right proof
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                check_proof= False
                new_proof +=1
        return new_proof
        
    # each block has is verified if its valid
    def hash(self, block):              #take the block and provide its hash
        encoded_block = json.dumps(block, sort_keys = True).encode() # encode the block so that sha can accept it
        return hashlib.sha256(encoded_block).hexdigest()      #hash of the block
        
    # is chain vaild function
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            # conditions
            # 1. To check if prev block hash = current block's previous hash
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            # 2. To check proof of work
            previous_proof = previous_block['proof']
            proof = block['proof'] # proof of current block
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] !='0000':
                return False
            previous_block = block
            block_index +=1
        return True
    
    
Mining the blockchain
# creating a web app using flask 
app = Flask(__name__)

#creating a blockchain
blockchain = Blockchain()

#mining the new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_prev_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congrats!', 
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Getting the full Blockchain displayed
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    
    return jsonify(response), 200

# running the app
app.run(host='0.0.0.0', port = 5000)
