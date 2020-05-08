# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 17:48:27 2020

@author: nishkal 
"""
#importing libraries and modules
import datetime
import hashlib
import json
from flask import Flask, jsonify
from flask.json import JSONEncoder

# Building the architecture of blockchain

class Blockchain:
    
    def __init__(self):
        self.chain=[] #chain contains a list of blocks linked together
        '''below is a function for creating a genesys block 
        which takes 2 args one for proof and other the key 
        which is hash of previous block.
        0 is in quotes as sha 256 accepts encoded characters'''
        self.create_block(proof=1, previous_hash='0')  
        
    #below is the function that is used for creating other blocks after mining
    def create_block(self, proof, previous_hash):
        block ={'index': len(self.chain)+1,
                'timestamp': str(datetime.datetime.now()),
                'proof':proof,
                'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    #get info of last block
    def get_previous_block(self):
        return self.chain[-1]
   

    #creating a proof of work for miners to mine a block

    def proof_of_work(self,previous_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            '''above operation is an algorithm which is hashed using sha 256
               inside the logic we must use a asymetric opertaion for proving 
               difficult cracking of the algorithm by the miners'''
            if hash_operation[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block=chain[0]
        block_index=1
        while block_index<len(chain):
            block = chain[block_index]
            if block['previous_hash']!= self.hash(previous_block):
                return False
            previous_proof=previous_block['proof']
            proof=block['proof']
            hash_operation=hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            previous_block = block
            block_index = block_index+1
        return True
    
# Mining the Blockchain
        
#creating a web app
class MiniJSONEncoder(JSONEncoder):
    """Minify JSON output."""
    item_separator = ','
    key_separator = ':'
    
app = Flask(__name__)
app.json_encoder = MiniJSONEncoder
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False       
#creating a Blockchain

blockchain = Blockchain()

@app.route('/mine_block', methods= ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message': 'Congrats, on mining a block, your block will be added to the blockchain',
                'index':block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash' : block['previous_hash']}

    return jsonify(response), 200

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    valid = blockchain.is_chain_valid(blockchain.chain)
    if valid == True:
        response = {'message':'The block is valid'}
    else:
        response = {'message':'The block is not valid'}
        
    return jsonify(response), 200



app.run(host='0.0.0.0',port = 5000)    
    