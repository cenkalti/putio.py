#! /usr/bin/env python

import re
import sys
import cmd
import logging
import traceback
import argparse
import putio2
from pprint import pprint
from pdb import set_trace as st


ROOT_ID = 0
ROOT_NAME = 'Your Files'


class PutioCLI(cmd.Cmd):
    
    def __init__(self, token):
        cmd.Cmd.__init__(self)
        self.prompt = '(put.io)$ '
        self.client =  putio2.Client(token)
        self.set_cwd(ROOT_ID, ROOT_NAME)
    
    # If this method is not overridden, it repeats the last nonempty command entered.
    def emptyline(self):
        pass

    def do_EOF(self, arg):
        PutioCLI.do_exit()
        
    @staticmethod
    def do_exit():
        print 'Bye!'
        sys.exit()

    def do_cd(self, filename):
        '''Change directory'''
        if filename:
            id = self.get_id_by_name(filename)
            self.set_cwd(id, filename)
        else:
            self.set_cwd(ROOT_ID, ROOT_NAME)

    def do_pwd(self, arg):
        '''Print working directory name'''
        print self.cwd_name

    def do_ls(self, filename):
        '''List current directory or directory given as parameter'''
        
        def print_files(files):
            line = '%10s  %12s  %25s  %s'
            print line % ('ID', 'Size', 'Created at', 'Name')
            for f in files.values():
                print line % (f.id, f.size, f.created_at, f.name)
                
        if filename:
            id = self.get_id_by_name(filename)
        else:    
            id = self.cwd_id
        
        files = self.client.File.list(id)
        
        if not filename:
            self.current_files = files
        
        print_files(files)
    
    def do_download(self, line):
        '''Download file to given destination.
        Usage: download <file_name> <destination>
            or download <file_id> <destination>
        If you give file_name it must be in current directory.'''
        args = re.split('\s+', line)
        filename = args[0]
        dest = args[1]
        
        if isinstance(filename, int):
            file = client.File({'id': filename})
        else:
            file = self.get_file_by_name(filename)
    
        file.download(dest)

    def complete_filename(self, text, line, begidx, endidx):
        self.load_current_files()
        return [f.name for f in self.current_files.values() if f.name.startswith(text)]
    
    def get_id_by_name(self, filename):
        return self.get_file_by_name(filename).id
    
    def get_file_by_name(self, filename):
        self.load_current_files()
        for f in self.current_files.values():
            if f.name == filename:
                return f
        raise Exception('No file')
    
    def load_current_files(self):
        if not self.current_files:
            self.current_files = self.client.File.list(self.cwd_id)
    
    def set_cwd(self, id, name):
        self.cwd_id = id
        self.cwd_name = name
        self.current_files = None

    complete_cd = complete_filename
    complete_ls = complete_filename
    complete_download = complete_filename


def main():
    parser = argparse.ArgumentParser(description = 'Put.io Console')
    parser.add_argument('token')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)  

    cli = PutioCLI(args.token)
    cli.cmdloop()


if __name__ == '__main__':
    main()
