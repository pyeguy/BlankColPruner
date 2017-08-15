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
	bad_cols = []
	for col in cols:
		nulls = sum(df[col].isnull().values)
		if nulls >= empty_threshold:
			bad_cols.append(col)
	df.drop(bad_cols,axis=1,inplace=True)
	print("Dropped {} cols".format(len(bad_cols)))
	return df
	

def infer_delim(fname):
	fnamecomps = fname.lstrip('.').lstrip('/').lstrip('\\').split('.')
	fext = fnamecomps[1]
	
	if fext.lower() == 'csv':
		delim = ','
	elif fext.lower() == 'tab':
		delim = '\t'
	else:
		delim = None	

	return delim

def load_and_prune(fname,path,**kwargs):
	# fnamecomps =fname.split('.')
	try:
		delim = kwargs['delim']
	except KeyError:
		delim = infer_delim(fname)

	df = pd.read_table(os.path.join(path,fname),delimiter=delim)
	print("Pruning : {}".format(fname))
	pdf = prune_df(df,kwargs['empty_threshold'])
	return pdf

if __name__ == '__main__':
	parser = argparse.ArgumentParser(prog='Blank Col Pruner')
	parser.add_argument('input',help="input file or folder.")
	parser.add_argument('-s','--suffix',help="custom file suffix for the output files (default is '_pruned'",default='_pruned')
	parser.add_argument('-t','--threshold',help='the number of empty rows to be considered a column to prune',default=1000,type=int)
	args = parser.parse_args()

	# prune_df = lambda x:prune_df(x,args.threshold)

	if os.path.isfile(args.input):
		fnamecomps = args.input.lstrip('.').lstrip('/').lstrip('\\').split('.')
		pdf = load_and_prune(fname=args.input,path='',empty_threshold=args.threshold)
		delim = infer_delim(args.input)
		pdf.to_csv(fnamecomps[0]+args.suffix+'.'+fnamecomps[1],sep=delim)

	elif os.path.isdir(args.input):
		walker = os.walk(args.input)
		root, dirs, files = next(walker)

		for fname in files:
			fnamecomps = fname.lstrip('.').lstrip('/').lstrip('\\').split('.')
			pdf = load_and_prune(fname=fname,path=root,empty_threshold=args.threshold)
			delim = infer_delim(fname)
			pdf.to_csv(os.path.join(root,fnamecomps[0]+args.suffix+'.'+fnamecomps[1]),sep=delim)
	else:
		raise Exception('Unkown input type. Must be file or dir.')

