
from blankcolpruner import *

import argparse,os


def main():
	parser = argparse.ArgumentParser(prog='Blank Col Pruner')
	parser.add_argument('input',help="input file or folder.")
	parser.add_argument('-s','--suffix',help="custom file suffix for the output files (default is '_pruned'",default='_pruned')
	parser.add_argument('-t','--threshold',help='the number of empty rows to be considered a column to prune',default=1000,type=int)
	args = parser.parse_args()

	# prune_df = lambda x:prune_df(x,args.threshold)

	if os.path.isfile(args.input):
		fnamecomps = _filenamecomps(args.input)
		pdf = load_and_prune(fname=args.input,path='',empty_threshold=args.threshold)
		delim = infer_delim(args.input)
		pdf.to_csv(fnamecomps[0]+args.suffix+'.'+fnamecomps[1],sep=delim)

	elif os.path.isdir(args.input):
		walker = os.walk(args.input)
		root, dirs, files = next(walker)
		outputpath = os.path.join(root,args.suffix.lstrip('_'))
		try:
			os.mkdir(outputpath)
		except:
			print("Folder already exists, files will be overwritten")

		for fname in files:
			fnamecomps = _filenamecomps(fname)
			pdf = load_and_prune(fname=fname,path=root,empty_threshold=args.threshold)
			delim = infer_delim(fname)
			pdf.to_csv(os.path.join(outputpath,fnamecomps[0]+args.suffix+'.'+fnamecomps[1]),sep=delim)
	else:
		raise Exception('Unkown input type. Must be file or dir.')	

if __name__ == "__main__":
	main()