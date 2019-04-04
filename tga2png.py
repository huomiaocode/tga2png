#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import time
import optparse
import threading
from PIL import Image


def thread_run(file_list, max_thread_count=10):
    start = time.time()
    obj = {
        "threadLock": threading.Lock(),
        "threads": [],
        "index": 0,
    }
    
    file_count = len(file_list)

    def run():
        while obj["index"] < file_count:
            fileRealPath, fileToPath = file_list[obj["index"]]
            idx = obj["index"]

            obj["threadLock"].acquire()
            obj["index"] += 1
            obj["threadLock"].release()
            
            if os.path.exists(fileToPath):
                print("%s is exist pass" % fileToPath)
                continue
            
            print("%s/%s  %s -> %s" % (idx, file_count, fileRealPath, fileToPath))
            fileToFolder = os.path.dirname(fileToPath)
            if not os.path.exists(fileToFolder):
                os.makedirs(fileToFolder)
            
            Image.open(fileRealPath).save(fileToPath)

    for _ in xrange(max_thread_count):
        t = threading.Thread(target=run)
        t.start()
        obj["threads"].append(t)

    for t in obj["threads"]:
        t.join()

    end = time.time()
    print "thread_run, duration %s" % (end - start)

def convert(folderFrom, folderTo):
    folderFrom = os.path.realpath(folderFrom)
    folderTo = os.path.realpath(folderTo)
    
    print("convert from %s to %s" % (folderFrom, folderTo))
    
    # [(fileFrom, fileTo)]
    file_list = []
    
    for root, dirs, files in os.walk(folderFrom):
        for filePath in files:
            if filePath.endswith(".tga"):
                fileRealPath = os.path.realpath(root + "/" + filePath)
                fileToPath = os.path.realpath(folderTo + "/" + root[len(folderFrom):] + "/" + filePath[:-len(".tga")] + ".png")
                
                file_list.append((fileRealPath, fileToPath))
    
    thread_run(file_list, 30)
               
    print("convert end.")


if __name__ == "__main__":
    parse = optparse.OptionParser()
    parse.add_option("-f", "--from", dest="from_folder", help="input image input path")
    parse.add_option("-t", "--to", dest="to_folder", help="input image output path")
    
    (options, args) = parse.parse_args(sys.argv)
    
    if options.from_folder != None and options.to_folder != None:
        convert(options.from_folder, options.to_folder)