#! /usr/bin/env python

import re
import sys
import logging
import traceback
import argparse
import putio2
from pprint import pprint
from pdb import set_trace as st


client = None
cwd = 0


def handle_help(*args):
    print 'Supported commands:'
    print '  exit'
    print '  ls'
    print '  download'


def handle_exit(*args):
    print 'Bye!'
    sys.exit()


def handle_cd(*args):
    global cwd
    cwd = args[0]


def handle_pwd(*args):
    print cwd


def handle_ls(*args):
    files = client.File.list(cwd)
    
    for f in files.values():
        print '%s\t%s' % (f.id, f.name)


def handle_download(*args):
    file_id = args[0]
    dest = args[1]
    
    client.File({'id': file_id}).download(dest)


def main():
    parser = argparse.ArgumentParser(description = 'Put.io Console')
    parser.add_argument('token')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    global client
    client = putio2.Client(args.token)    

    while True:
        try:
            try:
                line = raw_input('$ ')
            except EOFError:
                handle_exit()
        
            if not line:
                continue
        
            args = re.split('\s+', line)
        
            cmd = args[0]
            args = args[1:]
        
            try:
                handler = globals()['handle_%s' % cmd]
            except KeyError:
                print 'Unknown command. For a list of supported commands enter "help"'
            else:
                handler(*args)
        except KeyboardInterrupt:
            break
        except Exception as e:
            traceback.print_exc(e)
