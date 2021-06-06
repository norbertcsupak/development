### Objective:  File(or folder) compress with tar-gz , or decompress it 

### Usage for compress : 

```
python targz.py comp -h
usage: targz.py comp [-h] -f FOLDER -n NAME

compress command

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        list of folder or files to be compressed (comma separated lits)
  -n NAME, --name NAME  name of the output file

```

exaple: python targz.py comp -f myfolder,myfile.txt -n my_compressed.tar.gz

### Usage for decopress: 

```
python targz.py decomp -h
usage: targz.py decomp [-h] -i INPUT -o OUTPUT

decompress command

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        fileneme to decompress
  -o OUTPUT, --output OUTPUT
                        location wheret to extract

```
exapmle: python targz.py decomp -i my_compressed.tar.gz -o /tmp/
