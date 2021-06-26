import tarfile
from tqdm import tqdm
import os
import argparse

parser = argparse.ArgumentParser(description='file or folder -> compress or decompress *.tar.gz files|folder')
subparser = parser.add_subparsers(dest='command')


compress=subparser.add_parser('comp',description=' compress command')
decompress=subparser.add_parser('decomp',description=' decompress command')


compress.add_argument('-f', '--folder',type=str, help='list of folder or files to be compressed (comma separated lits) ',required=True)
compress.add_argument('-n', '--name',type=str, help='name of the output file',required=True)


decompress.add_argument('-i', '--input',type=str, help='fileneme to decompress',required=True)
decompress.add_argument('-o', '--output',type=str, help='location wheret to extract ',required=True)

args = parser.parse_args()


def compress(tar_files, members):
	# open a gzip  fro writing 
	tar = tarfile.open(tar_files, mode="w:gz")

	# set progress bar 
	progress=tqdm(members)
	for member in progress:
		# adding file or folder  to the tar file 
		tar.add(member)
		progress.set_description(f"Compressing {member}")
	tar.close()


def decompress(tar_file, path, members=None):
	tar=tarfile.open(tar_file, mode="r:gz")
	if members is None:
		members=tar.getmembers()

	progress=tqdm(members)
	for member in members:
		tar.extract(member,path=path)
		progress.set_description(f"Extracting {member.name}")
	tar.close()

if __name__ == '__main__':
	if args.command == 'comp':
		
		file_list = [str(item) for item in args.folder.split(',')]
		compress(args.name, file_list)

	if args.command == 'decomp':
		decompress(args.input,args.output)