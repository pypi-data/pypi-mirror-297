import sys

def show_python_help():
    objs = sys.argv[1:]
    for obj in objs:
        help(obj)
