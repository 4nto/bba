import os, re

class Clean:
	pass

def command_exist(fpath):
	return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

'''
haridsv from stackoverflow
http://stackoverflow.com/questions/1714027/version-number-comparison
'''
def version_cmp(version1, version2):
    def normalize(v):
        return map (int, re.sub (r'(\.0+)*$','', v).split("."))
    return cmp (normalize(version1), normalize(version2))