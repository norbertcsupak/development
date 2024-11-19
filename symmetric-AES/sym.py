"""
based on :

https://www.thepythoncode.com/article/encrypt-decrypt-files-symmetric-python
"""

from cryptography.fernet import Fernet
import argparse

"""
parserX = argparse.ArgumentParser(description='Symetric file encode - decode')
parserX.add_argument('--targetd',type=str,help='target directory to  place the grabbed  files',required=True)
args = parserX.parse_args()
"""

def write_key(mykey):
	"""
	creating a fernet key here 
	"""

	key = Fernet.generate_key()
	with open(mykey,"wb") as key_file:
		key_file.write(key)

def load_my_key(mess):
	"""
	Load my  previously created key
	"""
	print(f'Key loaded ...{mess}')
	return open("mykey.key","rb").read()

def encrypt(filename, mykey):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(mykey)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=' option to create or user a key')
	"""
	List of commands:
	 create  (this create key file)
	 crypt   (this will  crypt a file)
	 decrypt (this will decrypt yotu file )
	"""

	subparsers = parser.add_subparsers()
	"""
	make a subparsers for create ,  crypt and  decrypting
	"""


	parser_create = subparsers.add_parser('create', help='create Fernet key')
	parser_create.add_argument('--file', dest='mykey', required=True, type=str, help='Key name to write')
	parser_create.set_defaults(function=write_key)

	parser_crypt = subparsers.add_parser('crypt', help='crypting a file')
	parser_crypt.add_argument('--keyfile', required=True, type=str, help='define key file to use')
	parser_crypt.add_argument('--file', type=str, required=True, help=' file name to crypt with fernet key')
	parser_crypt.set_defaults(function=load_my_key)

	parser_decrypt = subparsers.add_parser('decrypt', help='decrypting a file')
	parser_decrypt.add_argument('--keyfile', required=True, type=str, help='use a key file to use')
	parser_decrypt.add_argument('--file', type=str, required=True, help=' file name to decrypt with fernet key')
	

	arguments = parser.parse_args()
	print(arguments)
	arguments.function()
