#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
from PIL import Image
import optparse

def convert(folderFrom, folderTo):
    folderFrom = os.path.realpath(folderFrom)
    folderTo = os.path.realpath(folderTo)
    
    print("convert from %s to %s" % (folderFrom, folderTo))
    
    for root, dirs, files in os.walk(folderFrom):
        for filePath in files:
            if filePath.endswith(".tga"):
                fileRealPath = os.path.realpath(root + "/" + filePath)
                fileToPath = os.path.realpath(folderTo + "/" + root[len(folderFrom):] + "/" + filePath[:-len(".tga")] + ".png")
                
                if os.path.exists(fileToPath):
                    print("%s is exist pass" % fileToPath)
                    continue
                
                print("%s -> %s" % (fileRealPath, fileToPath))
                fileToFolder = os.path.dirname(fileToPath)
                if not os.path.exists(fileToFolder):
                    os.makedirs(fileToFolder)
                
                Image.open(fileRealPath).save(fileToPath)
               
    print("convert end.")


if __name__ == "__main__":
    parse = optparse.OptionParser()
    parse.add_option("-f", "--from", dest="from_folder", help="input image input path")
    parse.add_option("-t", "--to", dest="to_folder", help="input image output path")
    
    (options, args) = parse.parse_args(sys.argv)
    
    if options.from_folder != None and options.to_folder != None:
        convert(options.from_folder, options.to_folder)