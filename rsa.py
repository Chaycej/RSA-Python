import os
import random
import sys

def modexp(a, b, c):

    def ndigits(n, b):
        digits = []
        while n:
            digits.append(n % b)
            n = int(n/b)
        return digits

    base = 2 << (4)

    table = [1] * base
    for i in range(1, base):
        table[i] = table[i-1] * a % c

    r = 1
    digits = ndigits(b, base)[::-1]

    for digit in digits:
        for i in range(5):
            r = r * r % c
        
        if digit:
            r = r * table[digit] % c
    return r

def miller_rabin(n, k, witness=None):

    if n % 2 == 0:
        return 0

    if witness is not None:
        if primality(n, witness) == 0:
            return 0
        return 1

    for i in range(1, k+1):

        # Pick a random witness
        a = random.randint(2, n-1)
        if primality(n, a) == 0:
            return 0
    return 1


def primality(n, a):
    num = n-1
    count = 0

    # Find first odd number
    while num % 2 == 0:
        num //= 2
        count += 1
    
    res = modexp(a, num, n)
    if res == 1:
        return 1

    while count > 0:
        if res == n-1:
            return 1
        res = (res * res) % n
        count -= 1
    return 0

def key_generation(public_path, private_path):
    if os.path.isfile(public_path):
        print("There is already a public and private key generated")
        print("To generate new keys, delete the public/private key files")
        return

    seed = int(input("Type a number to use as a seed: "))

    random.seed(seed)
    prime = None

    while prime is None:
        q = random.randint(2**31, 2**32)
        if miller_rabin(q, 25) == 1:
            if q % 12 == 5 and miller_rabin((q * 2) + 1, 25) == 1:
                prime = (q * 2) + 1

    priv_key = random.randint(1, prime-1)
    g = 2
    e2 = modexp(g, priv_key, prime)

    pubk_file = open(public_path, "w")
    privk_file = open(private_path, "w")
    pubk_file.write("{prime} {g} {e2}".format(prime=prime, g=g, e2=e2))
    privk_file.write("{prime} {g} {priv_key}".format(prime=prime, g=g, priv_key=priv_key))

def encrypt(plaintext_path, output_path, pubkey_path):
    pubk_file = open(pubkey_path, "r")
    p, g, e2 = pubk_file.read().split(" ")
    p, g, e2 = int(p), int(g), int(e2)

    text_file = open(plaintext_path, "r")
    output_file = open(output_path, "w")
    content = text_file.read()
    for c in content:
        k = random.randint(1, p-1)
        c1 = modexp(g, k, p)
        c2 = (modexp(e2, k, p) * (ord(c) % p)) % p
        print("c1, c2 = ", c1, c2)
        output_file.write("{c1} {c2} ".format(c1=c1, c2=c2))

def decrypt(encrypted_path, output_path, privkey_path):
    privk_file = open(privkey_path, "r")
    p, g, d = privk_file.read().split(" ")
    p, g, d = int(p), int(g), int(d)
    crypt_file = open(encrypted_path, "r")
    output_file = open(output_path, "w")
    content = crypt_file.read().split(" ")

    index = 0
    retstr = ""
    while index < len(content)-1:
        c1 = int(content[index])
        c2 = int(content[index+1])
        m = (modexp(c1, p-1-d, p) * (c2 % p)) % p
        retstr += chr(m)
        index += 2

    print(retstr)
    output_file.write(retstr)

def main():

    if len(sys.argv) < 2:
        print("Must specify an rsa mode")
        print("k - key generation")
        print("e - encryption")
        print("d - decryption")
        return

    mode = sys.argv[1]

    # Key generation mode
    if mode == "k":

        if len(sys.argv) < 4:
            print("Must specify the file paths of the public and private keys")
            print("python3 rsa.py k <public key> <private key>")
            return

        key_generation(sys.argv[2], sys.argv[3])

    # Encryption mode
    elif mode == "e":

        if len(sys.argv) < 5:
            print("Invalid command arguments")
            print("python3 rsa.py e <plaintext file> <output file> <public key file>")
            return

        if os.path.isfile(sys.argv[2]) == False:
            print("No plaintext file found for:", sys.argv[2])
            return

        if os.path.isfile(sys.argv[3]):
            print("Cannot encrypt. An encrypted file already exists")
            print("Delete", sys.argv[3], " to encrypt")
            return

        if os.path.isfile(sys.argv[4]) == False:
            print("Invalid public key path")
            return
        
        encrypt(sys.argv[2], sys.argv[3], sys.argv[4])

    # Decryption mode
    elif mode == "d":

        if len(sys.argv) < 5:
            print("Invalid command arguments")
            print("python3 rsa.py d <encrypted file> <output file> <private key file>")
            return

        if os.path.isfile(sys.argv[2]) == False:
            print("Cannot decrypt. Need a valid encrypted file")
            return

        if os.path.isfile(sys.argv[4]) == False:
            print("Invalid private key path")
            return
        
        decrypt(sys.argv[2], sys.argv[3], sys.argv[4])

    else:
        print("Unknown rsa mode")

if __name__ == "__main__":
    main()