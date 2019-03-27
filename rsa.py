import os
import random
import sys


primes = [7681, 7687, 7691, 7699, 7703, 7717, 7723, 7727, 7741, 7753, 7757, 7759, 7789,
7793, 7817, 7823, 7829,7841, 7853, 7867, 7873, 7877,7879, 7883, 7901, 7907, 7919]

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
    
    res = pow(a, num, n)
    if res == 1:
        return 1

    while count > 0:
        if res == n-1:
            return 1
        res = (res * res) % n
        count -= 1
    return 0

def key_generation():
    seed = input("Type a number to use as a seed: ")
    seed = int(seed)

    random.seed(seed)
    pub_key = None

    while pub_key is None:
        randnum = random.randint(1000000, 1000000000)
        if miller_rabin(randnum, 25) == 1:
            if randnum % 12 == 5 and miller_rabin((randnum * 2) + 1, 25) == 1:
                pub_key = randnum

    priv_key = random.randint(1, pub_key-1)
    g = 2
    e2 = pow(g, priv_key, pub_key)

def main():
    print("k : key generation")
    print("e : encryption")
    print("d : decryption")
    mode = input("Choose a mode: ")

    if mode == "k":
        key_generation()


if __name__ == "__main__":
    main()
