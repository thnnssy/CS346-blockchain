import hashlib
import secrets
import time
from ProofOfWork import *

#
#  This Python code demonstrates the "Distributed Ledger" aspect of
#   the blockchain technology. This is how the blockchain is verified and
#   how people are able to "own" a part of the blockchain if it is being
#   used as digital currency..
#

#
#  Some of this code adapted from: https://github.com/davecan/easychain/blob/master/blockchain.py
#   and from: https://towardsdatascience.com/build-your-own-blockchain-protocol-for-a-distributed-ledger-54e0a92e1f10
#

#
#  In the context of a blockchain currency, "transaction" is typically abbreviated to TX.
#
#  Transactions accrue on the network, waiting for a new block to go through so that they can
#   be validated (they are attached to the block.) This is the distributed ledger. Everyone, even
#   people who do not own any Bitcoin, can see all the transactions that have ever been made, since
#   they are recorded into the blockchain itself.
#

#
# In this simplified version, we simply attach one transaction to one block.
#  However, we can see that the chain of transactions becomes longer and longer.
#
# If someone wanted to alter the chain, and what the transactions say, could they?
#
# The answer, at least in the case of Bitcoin, is probably not. The amount of computing
#  power they would need would be in excess of half of all miners computing power on the
#  network. However, if they could somehow acquire that much computing power, they could
#  temporarily control all new blocks being added to the chain, which would be very bad for
#  the validity of the currency.
#

class TX:

    # In the case of the sender and receiver, in a real blockchain network, we would
    #  use unique digital signatures instead of names. However in this example we will
    #  use simple names, Bob and Sue.

    def __init__(self, tx_amount, sender, receiver):
        self.tx_amount = tx_amount
        self.timestamp = time.time()
        self.sender = sender
        self.receiver = receiver

    def __str__(self):
        return "TX[" + ":".join([
            str(self.tx_amount),
            str(self.timestamp),
            str(self.sender),
            str(self.receiver),
        ]) + "]"

    def __rpr__(self):
        return str(self)

class block:

    # In blockchain, the transactions will be stored in the next block.
    #  Invalid transactions are prevented by the protocol itself;
    #  there is no risk of double spending or unsigned transactions.

    # In this case, the nonce is not actually what proves the work has
    #  been done, necessarily. It is the HASH that resulted in that nonce,
    #  that is important and must be placed into the block.
    # This is called the "hashed block header" and is used to identify the
    #  different blocks.

    def __init__(self, prev_block, transaction):
        self.prev_block = prev_block
        self.transaction = transaction

        self.hashSize = self.__get_hashSize()
        self.challengeLevel = self.__get_challengeLevel()

        self.nonce = ""

        # block_data consists of the previous block's nonce and a string
        # representation of the new transaction
        self.attempt_str, self.nonce = testAttempt(self.challengeLevel,
                                                   self.hashSize,
                                                   str(self.transaction))

    def validate(self):
        return (
            bool(self.nonce) and
            validateNonce(self.nonce, self.attempt_str, str(self.transaction))
        )

    def __get_hashSize (self):
        return 30

    def __get_challengeLevel (self):
        return 4

    def __str__(self):
        return f"block[nonce: {self.nonce}, prev: {self.prev_block.nonce}]"

    def __rpr__(self):
        return str(self)


class genesis_block(block):

    def __init__(self):
        self.nonce = secrets.token_hex()

    def validate(self):
        return True

    def __str__(self):
        return f"genesis_block[nonce: {self.nonce}]"


class block_chain:

    def __init__(self):
        self.blocks = []
        self.blocks.append(genesis_block())

    def addTx(self, new_tx):
        self.addBlock(block(self.lastBlock(), new_tx))

    def addBlock(self, new_block):
        # Verify the new block to be added.
        if new_block.prev_block == self.lastBlock() and new_block.validate():
            self.blocks.append(new_block)
        else:
            print("Failed to validate new block")

    def getBlock(self, index=-1):
        return self.blocks[-1]

    def lastBlock(self):
        return self.getBlock(-1)

    def __str__(self):
        return "block_chain:\n" + '\n'.join(str(b) for b in self.blocks)


def main ():
    print("------------------------------------------------")
    print("TEST: genesis_block")
    my_genblock = genesis_block()
    print("genesis_block nonce: my_genblock.nonce")
    print("SUCCESS")
    print("------------------------------------------------")
    print()

    print("------------------------------------------------")
    print("TEST: block")
    my_block = block(my_genblock, TX(5, "Sean", "Toby"))
    block_valid = my_block.validate()
    print("block.validate(): ", block_valid)
    if block_valid:
        print("SUCCESS: Block created and validated.")
    print("------------------------------------------------")
    print()

    print("------------------------------------------------")
    print("Testing class: block_chain")
    my_blockchain = block_chain()
    my_blockchain.addTx(TX(5, "Sean", "Toby"))
    my_blockchain.addTx(TX(5, "Toby", "Sean"))
    print(my_blockchain)
    print("------------------------------------------------")
    print()


if __name__ == "__main__" :
    main()
