import os, zipfile, shutil
from glob import glob as re

"""
file=
hash=$(file).sums
default:: build
size=2G
build: hash split
hash:
	@echo Creating a hash 512 of the file
	@sha512sum $(file) >> $(hash)
verify:
	@echo Verifying the sums file
	@shaa512sum -c $(hash)
split:
	@echo Splitting the original file
	@split -b $(size) --verbose $(file) split_file_
	@echo Zipping files
	@for f in split_file_*;do echo $$f;7z a $$f.zip $$f -sdel -mx=0;done
join:
	@echo Unzipping files
	@for f in split_file_*zip;do echo $$f;7z x $$f;done
	@echo Removing all of the *.zip files
	@rm split_file_*zip
	@echo Joining the files
	@cat split_file_* > $(file)
	@echo Removing the split files
	@rm split_file_*
	@echo Checking the hash file
	@sha512sum -c $(hash)
	#@echo Unzipping the files
	#@7z x $(file)
	@Removing the zip file
	@rm $(file)

"""

def readBin(foil):
	with open(foil,'rb') as reader:
		return reader.read()

def split(foil, CHUNK_SIZE = 100_000_000): #100MB
	foils_created = []
	succeeded = True

	if CHUNK_SIZE > 30653:
		CHUNK_SIZE = CHUNK_SIZE - 30653

	with open(foil,'rb') as f:
		try:
			chunk = f.read(CHUNK_SIZE)
			while chunk:
				current_file = foil.replace('.zip','') + '_broken_up_' + str(str( len(foils_created)+1 ).zfill(10))
				new_zip_file = current_file+".zip"

				with open(current_file, "wb+") as chunk_file:
					chunk_file.write(chunk)

				with zipfile.ZipFile(new_zip_file, 'w', compression=zipfile.ZIP_DEFLATED) as zip_file:
					zip_file.write(current_file, current_file)

				foils_created += [new_zip_file]
				os.remove(current_file)
				chunk = f.read(CHUNK_SIZE)

		except Exception as e:
			print(f"Exception :> {e}")
			succeeded = False

	if succeeded:os.remove(foil)

	return foils_created

def join(foil):
	try:

		mini_foils = re(str(foil).replace('.zip',"_broken_up_*.zip"))
		mini_foils.sort()

		for mini_foil in mini_foils:
			print(mini_foil)
			raw_foil = mini_foil.replace('.zip','')

			with zipfile.ZipFile(mini_foil,"r") as f:
				raw_foil = f.extract(member=raw_foil, path=os.path.dirname(mini_foil))

			current_content = readBin(raw_foil)

			with open(foil, 'ab+') as fp:
				fp.write(current_content)

			shutil.rmtree(os.path.dirname(raw_foil), ignore_errors=True)
			for foil_to_rm in [raw_foil, mini_foil]:
				if os.path.exists(foil_to_rm):
					os.remove(foil_to_rm)

		return foil
	except Exception as e:
		with open("err.txt", "w+") as writer:
			writer.write(str(e))
		print(e)

def arguments():
	import argparse
	parser = argparse.ArgumentParser(description=f"Enabling the capability to stretch a single large file into many smaller files, if both fiels are passed and the same file is passed, the split precedence is taken")
	parser.add_argument("--split", help="Split the specified file", nargs='?', type=str, default=None)
	parser.add_argument("--split_chunk", help="Split the specified file", nargs='?', type=int, default=100_000_000)
	parser.add_argument("--join", help="Recreate the specified file", nargs='?', type=str, default=None)
	return parser.parse_args()

def main():
	argz = arguments()
	does_exist = lambda file: os.path.exists(file)

	splits = None if argz.split is None or not does_exist(argz.split) else argz.split
	joins = None if argz.join is None else argz.join

	if splits is not None and joins is not None and splits == joins:
		joins = None

	if splits:
		split(
			foil=splits,
			CHUNK_SIZE=argz.split_chunk
		)

	if joins:
		join(
			foil=joins
		)

if __name__ == '__main__':
	main()
