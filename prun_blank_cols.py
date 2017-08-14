import pandas as pd
import argparse, os

# try:
# 	from tqdm import tqdm
# except:
# 	pass



def prune_df(df,empty_threshold):
	'''
	prune a dataframe to only the columns which have fewer than the threshold empty cells
	Args:
		df : dataframe with columns to be pruned
		empty_threshold : how many empty values to be considered a bad column
	Returns:
		pdf : pruned dataframe
	'''
	cols = list(df.columns)
	


def load_and_prune(fname,path,**kwargs):
	fnamecomps =fname.split('.')
	fext = fnamecomps[1]
	
	if 'delim' in kwargs:
		delim = kwargs['delim']
	elif fext.lower() == 'csv':
		delim = ','
	elif fext.lower() == 'tab':
		delim = '\t'
	else:
		delim = None
	
	df = pd.read_table(path+fname,delimiter=delim)
	print("Pruning : {}".format(fname))
	pdf = prune_df(df)
	return pdf

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='Blank Col Pruner')
	parser.add_argument('input',help="input file or folder.")
	parser.add_argument('-s','--suffix',help="custom file suffix for the output files (default is '_pruned'",default='_pruned')
	parser.add_argument('-t','--threshold',help='the number of empty rows to be considered a column to prune',default=1000,type=int)
	args = parser.parse_args()

	prune_df = lambda x:prune_df(x,args.threshold)

	if os.path.isfile(args.input):
		pdf = load_and_prune(fname=args.input,path='')
		pdf.to_csv(args.input+args.suffix)

	elif os.path.isdir(args.input):
		walker = os.walk(args.input)
		root, dirs, files = next(walker)

		for fname in files:
			pdf = load_and_prune(fname=fname,path=root)
			pdf.to_csv(root+fname+args.suffix)
	else:
		raise Exception('Unkown input type. Must be file or dir.')

