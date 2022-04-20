import hashlib
import time
import datetime


# Block
class Block:

    # Initial
    def __init__(self, index, proof_no, prev_hash, data, timestamp = None):
        # position of the block within the blockchain
        self.index = index
        # the number produced during the creation of a new block (called mining)
        self.proof_no = proof_no
        # refers to the hash of the previous block within the chain
        self.prev_hash = prev_hash
        # gives a record of all transactions completed, such as the quantity bought
        self.data = data
        # places a timestamp for the transactions
        self.timestamp = timestamp or time.time()

    # Calculate hash
    @property
    def calculate_hash(self):
        block_of_string = f"{self.index}{self.proof_no}{self.prev_hash}{self.data}{self.timestamp}"


        return hashlib.sha256(block_of_string.encode()).hexdigest()

    # repr
    def __repr__(self):
        return f"{self.index} - {self.proof_no} - {self.prev_hash} - {self.data} - {self.timestamp}"


# Chaining blocks
class BlockChain:

    # Initial
    def __init__(self):
        # keeps all blocks
        self.chain = []
        # keeps all the completed transactions in the block
        self.current_data = []
        self.nodes = set()
        # initial block
        self.construct_genesis()

    # Initial block
    def construct_genesis(self):
        self.construct_block(proof_no = 0, prev_hash = 0)

    # Create block
    def construct_block(self, proof_no, prev_hash):
        block = Block(
            index = len(self.chain),
            proof_no = proof_no,
            prev_hash = prev_hash,
            data = self.current_data)
        self.current_data = []

        self.chain.append(block)
        return block

    # Check validation
    @staticmethod
    def check_validity(block, prev_block):
        if prev_block.index + 1 != block.index:
            return False

        elif prev_block.calculate_hash != block.prev_hash:
            return False

        elif not BlockChain.verifying_proof(block.proof_no,
                                            prev_block.proof_no):
            return False

        elif block.timestamp <= prev_block.timestamp:
            return False

        return True

    # New data
    def new_data(self, sender, recipient, quantity):
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })
        return True

    # Proof
    @staticmethod
    def proof_of_work(last_proof):
        '''
         Proof of work is a concept that prevents the blockchain from abuse. Simply, its objective is to identify a number that solves a problem after a certain amount of computing work is done.
         If the difficulty level of identifying the number is high, it discourages spamming and tampering with the blockchain.
         In this case, we’ll use a simple algorithm that discourages people from mining blocks or creating blocks easily.

         this simple algorithm identifies a number f' such that hash(ff') contain 4 leading zeroes
         f is the previous f'
         f' is the new proof
        '''
        proof_no = 0
        while BlockChain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1

        return proof_no

    @staticmethod
    def verifying_proof(last_proof, proof):
        #verifying the proof: does hash(last_proof, proof) contain 4 leading zeroes?

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    # Latest block
    @property
    def latest_block(self):
        return self.chain[-1]

    # Mining block
    def block_mining(self, details_miner):

        self.new_data(
            sender = "0",  #it implies that this node has created a new block
            receiver = details_miner,
            quantity = 1,  #creating a new block (or identifying the proof number) is awarded with 1
        )

        last_block = self.latest_block

        last_proof_no = last_block.proof_no
        proof_no = self.proof_of_work(last_proof_no)

        last_hash = last_block.calculate_hash
        block = self.construct_block(proof_no, last_hash)

        return vars(block)

    # Create node
    def create_node(self, address):
        self.nodes.add(address)
        return True


    @staticmethod
    def obtain_block_object(block_data):
        #obtains block object from the block data

        return Block(
            block_data['index'],
            block_data['proof_no'],
            block_data['prev_hash'],
            block_data['data'],
            timestamp = block_data['timestamp'])


# Transaction
class Transaction:
    def __init__(self,from_wallet,to_wallet,amount):
        self.from_wallet = from_wallet
        self.to_wallet = to_wallet
        self.amount = amount



