'''
Command Line script for pruning columns from tabular datasets w/ blank values.

Take arguments for specifying number of blank values threshold for pruning and custom suffix for filenames.
'''
from blankcolpruner import *

import argparse,os


def main():
	# arg parsing
	parser = argparse.ArgumentParser(prog='Blank Col Pruner')
	parser.add_argument('input',help="input file or folder.")
	parser.add_argument('-s','--suffix',help="custom file suffix for the output files (default is '_pruned'",default='_pruned')
	parser.add_argument('-t','--threshold',help='the number of empty rows to be considered a column to prune',default=1000,type=int)
	args = parser.parse_args()

	# check and see if the input was a file
	if os.path.isfile(args.input):
		fnamecomps = _filenamecomps(args.input)
		pdf = load_and_prune(fname=args.input,path='',empty_threshold=args.threshold)
		delim = infer_delim(args.input)
		if not delim:
			delim = '\t'
		pdf.to_csv(fnamecomps.filename + args.suffix + '.' + fnamecomps.ext,
				sep=delim)

	# check and see if input was a folder
	elif os.path.isdir(args.input):
		walker = os.walk(args.input)
		root, dirs, files = next(walker)
		outputpath = os.path.join(root,args.suffix.lstrip('_'))
		
		# try and make output folder, if already exists then files will be overwritten
		try:
			os.mkdir(outputpath)
		except:
			print("Folder already exists, files will be overwritten")
		
		# iterate through files in folder 
		# TODO add some exception handling in here for files that aren't data
		for fname in files:
			fnamecomps = _filenamecomps(fname)
			pdf = load_and_prune(fname=fname,path=root,empty_threshold=args.threshold)
			delim = infer_delim(fname)
			if not delim:
				delim = '\t'
			pdf.to_csv(os.path.join(outputpath,
				fnamecomps.filename + args.suffix + '.' + fnamecomps.ext),
				sep=delim)
	# bad input
	else:
		raise Exception('Unkown input type. Must be file or dir.')	

if __name__ == "__main__":
	main()