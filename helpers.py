from os import walk,path,listdir,chmod
import stat

def pdirs(folder):
	for l in listdir(folder):
		chmod(folder, stat.S_IWRITE)
	return listdir(folder)
	directory_list = list()
	for root, dirs, files in walk(folder, topdown=False):
		for name in dirs:
			l=path.join(root, name)
			chmod(name, stat.S_IWRITE)
			directory_list.append(l)
			for file in files:
				chmod(path.join(l, file), stat.S_IWRITE)
	return directory_list
def pfnames(dir,search=None):
	if search is None:
		return next(walk(self.base_dir), (None, None, []))[2]  # [] if no file
	else:
		fnames = next(walk(self.base_dir), (None, None, []))[2]
		if search in fnames:
			return seach
		else:
			return search+'not found'