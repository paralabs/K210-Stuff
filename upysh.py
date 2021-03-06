import sys
import os

class LS:

    def __repr__(self):
        self.__call__()
        return ""

    def __call__(self, path="."):
        l = [_ for _ in os.ilistdir(path)]
        l.sort()
        for f in l:
            if f[1] == 0x4000:  # stat.S_IFDIR
                print("   <dir> %s" % f[0])
        for f in l:
            if f[1] != 0x4000:
                print("% 8d %s" % (f[3], f[0]))
        st = os.statvfs(path)
        print("\n{:,d}k free".format(st[0] * st[3] // 1024))

class PWD:

    def __repr__(self):
        res = os.getcwd()
        if res == "": # TLD on esp8266
            res = "/"
        return res

    def __call__(self):
        return self.__repr__()

class CLEAR:

    def __repr__(self):
        return "\x1b[2J\x1b[H"

    def __call__(self):
        return self.__repr__()

class MAN:

    def __repr__(self):
        return("""
upysh is intended to be imported using:
from upysh import *

To see this help text again, type "man".

upysh commands:
pwd, cd("new_dir"), ls, ls(...), head(...), cat(...), hexdump(...)
newfile(...), mv("old", "new"), rm(...), mkdir(...), rmdir(...)
clear
""")

    def __call__(self):
        return self.__repr__()


def head(f, n=10):
    with open(f) as f:
        for i in range(n):
            l = f.readline()
            if not l: break
            sys.stdout.write(l)

def cat(f):
    head(f, 1 << 30)

def newfile(path):
    print("Type file contents line by line, finish with EOF (Ctrl+D).")
    content = []
    while 1:
        try:
            content.append(input())
        except EOFError:
            break
    f = open(path, "w")
    f.write('\n'.join(content))
    f.write('\n')
    f.close()


def hexdump(file, length=16):

    with open(file, "rb") as f:
        c = 0
        while True:
            chars = f.read(length)
            if len(chars) == 0:
                return
            print('%04x %-*s %s' % (c, length*3, 
                  ' '.join(['%02x' % x for x in chars]),
                  ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in chars])))
            c += len(chars)


def rm(d):  # Remove file or tree

    try:
        if os.stat(d)[0] == 16384:  # Dir
            for f in os.ilistdir(d):
                rm("/".join((d, f[0])))  # File or Dir
            os.rmdir(d)
        else:  # File
            os.remove(d)
    except:
        print("rm of '%s' failed" % d)


pwd = PWD()
ls = LS()
clear = CLEAR()
man = MAN()
cd = os.chdir
mkdir = os.mkdir
mv = os.rename
rmdir = os.rmdir

print(man)
