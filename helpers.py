from os import walk,path,listdir,chmod
import stat

def pdirs(path):
	# for l in listdir(path):
	# 	chmod(path, stat.S_IWRITE)
	return listdir(path)
	directory_list = list()
	for root, dirs, files in walk(path, topdown=False):
		for name in dirs:
			l=path.join(root, name)
			chmod(name, stat.S_IWRITE)
			directory_list.append(l)
			for file in files:
				chmod(path.join(l, file), stat.S_IWRITE)
	return directory_list
def pfnames(path,search=None):
	if search is None:
		return next(walk(path), (None, None, []))[2]  # [] if no file
	else:
		fnames = next(walk(path), (None, None, []))[2]
		if search in fnames:
			return seach
		else:
			return search+'not found'

def pdict(dct,padding=None,size=None,cols=None):
	tbl_str="\t\t"
	full=0.0
	if size is None:
		full=40.0
	else:
		full==size

	dict_size=len(dct)
	if padding==None:
		padding=round(full/dict_size)

	for i in range(dict_size):
		tbl_str+="{:<"+str(padding)+"} "

	if cols is not None:
		print (tbl_str.format(*cols))
	else:
		print (tbl_str.format(*list(dct.keys())))
	# print each data item.
	print (tbl_str.format(*list(dct.values())))

