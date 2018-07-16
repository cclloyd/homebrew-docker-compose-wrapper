#! /usr/local/bin/python3

import argparse
import sys
import os
import re
import types

# Version check
if sys.version_info < (3, 0):
    print("This tool requires python 3.")
    print("\tYou have: %s" % sys.version)
    sys.exit(1)

parser = argparse.ArgumentParser()



# Optional args
#parser.add_argument("-e", "--exclude", type=str, help="exclude compose file from command")
parser.add_argument("-e", "--exclude", nargs='*', default='', type=str, help="exclude compose file(s) or service(s) from command with a comma separated list")
parser.add_argument("-d", "--dir", default='compose', type=str, help="compose files directory")
parser.add_argument("-p", "--prod", action='store_true', help="production mode.")

# Positional args
parser.add_argument("command", nargs='*', help="docker-compose")
#parser.add_argument("options", help="docker-compose")


args = parser.parse_args()

print("exclude: %s" % args.exclude)
command = ""
for arg in args.command:
    command += "%s " % arg
args.command = command


compose_files = os.listdir(args.dir)
compose_dir = os.path.join(os.getcwd(), args.dir)


# Parse Excludes
#if isinstance(args.exclude, types.StringTypes):
#    args.exclude = args.exclude.split(',')
for exclude in args.exclude:
    for file in compose_files:
        if exclude.endswith('.yml'):
            if file == exclude:
                compose_files.remove(exclude)
        else:
            regex = re.compile("services:\s+(%s):" % exclude, re.MULTILINE)
            path = os.path.join(compose_dir, file)
            if len(regex.findall(open(path).read())) > 0:
                compose_files.remove(file)

for file in compose_files:
    regex = re.compile("#\s*exclude:\s* true", re.MULTILINE)
    path = os.path.join(compose_dir, file)
    if len(regex.findall(open(path).read())) > 0:
        compose_files.remove(file)


# Build command
command = "docker-compose %s " % args.command
for file in compose_files:
    command += " -f %s " % os.path.join(compose_dir, file)

command += args.command

#print("Compose files post: %s" % compose_files)
#print("excludes: %s" % args.exclude)
#print("Compose files post: %s" % compose_files)
os.system(command)



'''

TODO: Preparse arguments by getting command keyword and removing it from list and adding everything after it to string.


TODO: Add file "docker-compose-wrapper.yml" that allows for various run configurations (prod and dev)
TODO:  Add methods to build modes for docker-compose-wrapper.yml so you can build your own commands via this wrapper (like a testing mode that excludes ssl)
'''


