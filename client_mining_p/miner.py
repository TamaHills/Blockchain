import hashlib
import requests
import os
import sys
import json

coins = 0

# ascii escape sequence helpers to control console output
PURPLE = "\033[95m"
CYAN ="\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BRIGHT = '\033[97m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'

def clear():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')

def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while not valid_proof(block_string, proof):
        proof += 1
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    
    proof_string = f"{block_string}{proof}".encode()
    proof_hash = hashlib.sha256(proof_string).hexdigest()

    if proof_hash[:6] == '000000':
        return True
    else:
        return False


if __name__ == '__main__':
    clear()
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: Get the block from `data` and use it to look for a new proof
        # new_proof = ???
        new_proof = proof_of_work(data["block"])
        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data['message'] == 'new block forged':
            coins += 1
            print(f'{GREEN}{BOLD}new block forged.{END}{YELLOW}{BOLD} You have {coins} coins{END}')
        else:
            print(f'{RED}{BOLD}invalid or out of date pow{END}')
