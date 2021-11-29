import string
import random
import hashlib
import time

#
#  This Python code demonstrates the "Proof of Work" aspect of
#   the blockchain technology. This is how the blockchain grows,
#   and how mining is enabled for a blockchain.
#

#
#  Some of this code is adapted from: https://github.com/abdo1819/bitcoin_paper/blob/6f9035d07ff03f5988a7355d1187706f12f89395/proof%20of%20work.py
#


def generation (size) :
    attempt = ''.join(random.choice(string.ascii_lowercase +
                                    string.ascii_uppercase +
                                    string.digits) for i in range(size))

    return attempt


def testAttempt (challenge, hashSize) :
    nonceFound = False

    start = time.time()

    attemptCounter = 0
    while not nonceFound:
        attemptCounter += 1

        # The 'attempt' is the random string we are turning into bytes,
        #  in order to 'feed' it to the hash. The hash can only be 'fed'
        #  bytes. We feed it in order to keep guessing new numbers,
        #  hoping to find the nonce.
        attempt = generation(hashSize)

        # Here we are creating a hash object using the hashlib module
        #  of Python. The hash object is a new sequence which has been encrypted,
        #  and the hashing is (generally accepted to be) impossible to reverse.
        shaHash = hashlib.sha256()

        # This code converts our attempt into bytes so it can be fed to the hash.
        #  The hash cannot be fed strings, or other non-byte data types.
        #  UTF stand for Unicode Transformation Format.
        #  Here we use UTF-8, since it has the property that strings of ASCII text
        #  are also valid UTF-8 text, and it is a byte-oriented encoding method.
        b = bytes(attempt, 'utf-8')

        # This 'update' method is what changes our hash object, trying with a new
        #  random set of characters turned into bytes and being 'fed' to the front of it.
        shaHash.update(b)

        # This code converts the 'challenge' parameter into the number of
        #  zeroes we want to see at the front of the nonce for it to be considered valid.
        numZeros = ''
        for i in range (0,challenge) :
            numZeros += '0'

        # Finally, we use the hexdigest method. This 
        nonce = shaHash.hexdigest()

        if nonce.startswith(numZeros):
            print('The nonce looks like...\n',nonce,'\n')
            print('Finding nonce took: ', (time.time() - start), ' seconds.\n')

            nonceFound = True

    print('The final hash looks like...\n',shaHash,'\n')
    print('The string fed to the hash looks like...\n',attempt,'\n')
    print('Took ',attemptCounter,' attempts.')


def main():

    testAttempt(3, 20)


if __name__ == '__main__' :
    main()