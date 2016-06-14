from __future__ import print_function

import os
import sys




# def getFilePaths(directoryPath):
#     filePaths = []
#     count = 0
#     for subdir, dirs, files in os.walk(directoryPath):
#         for singleFile in files:
#             filepath = subdir + os.sep + singleFile

#             if (filepath.endswith(".mid")):
#                 filePaths.append(filepath)

#     return filePaths


def getFilePaths(directoryPath, extension):
    filePaths = []
    count = 0
    for subdir, dirs, files in os.walk(directoryPath):
        for singleFile in files:
        	if not singleFile.startswith('.'):
	            filepath = subdir + os.sep + singleFile

	            if (filepath.endswith(extension)):
                	filePaths.append(filepath)

    return filePaths


# print(data)

# fo = open("all_files", "wb")
# 	fo.write(data)
# 	fo.close()
# # for i in os.listdir(os.getcwd()):
# # 	print i