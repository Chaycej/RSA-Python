# RSA-Python

# Author
- Chayce Heiberg
- Chayce.Heiberg@wsu.edu

# About
This a Python script that implements the RSA algorithm for encrypting/decrytping ascii text files.
There are three modes, key generation, encryption, and decryption. Keys generated and output files
are specified by the user on the command-line.

# How to run
Key generation,
   - $ Python3 rsa.py k <public key file path> <private key file path>

Encryption,
   - $ Python3 rsa.py e <plaintext file path> <output file path> <public key file path>

Decryption,
   - $ Python3 rsa.py d <encrypted file path> <output file path> <private key file path>

# Archive

- rsa.py - Script for executing key generation and rsa algorithm
- README.md - Description file