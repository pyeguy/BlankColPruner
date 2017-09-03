import pandas as pd
import os
from collections import namedtuple

# try:
# 	from tqdm import tqdm
# except:
# 	pass

FileNameComps = namedtuple('FileNameComps','filename ext')

def _filenamecomps(localfilename):
	path,fname = os.path.slit(localfilename)
	fnamecomps = fname.split('.')
	if len(fnamecomps) == 1:
		fnamecomps.append('')
	return FileNameComps(fnamecomps)

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
	fnamecomps = _filenamecomps(fname)
	fext = fnamecomps.ext
	
	if fext.lower() == 'csv':
		delim = ','
	elif fext.lower() == 'tab':
		delim = '\t'
	else:
		delim = None	

	return delim

def load_and_prune(fname,path,**kwargs):
	try:
		delim = kwargs['delim']
	except KeyError:
		delim = infer_delim(fname)

	df = pd.read_table(os.path.join(path,fname),delimiter=delim)
	print("Pruning : {}".format(fname))
	pdf = prune_df(df,kwargs['empty_threshold'])
	return pdf



