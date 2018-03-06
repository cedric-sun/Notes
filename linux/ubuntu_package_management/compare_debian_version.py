# sudo apt-get install python-apt if module "apt_pkg" is not found

def compareV(a ,b):
    import apt_pkg
    apt_pkg.init()
    print("%s upstream version: %s" % (Va, apt_pkg.upstream_version(Va)))
    print("%s upstream version: %s" % (Vb, apt_pkg.upstream_version(Vb)))
    res = apt_pkg.version_compare(a,b)
    symbol = "?"
    if res > 0: symbol = '>'
    elif res == 0: symbol = '=='
    else: symbol = '<'
    print("%s %s %s" % (a,symbol,b))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Arguments error. See \"%s help\" for help" % sys.argv[0])
    elif sys.argv[2] == "help":
        print("2 Debian package version numbers is required as arguments.")
        print("Legend: ?unknown, >greater_than, <smaller_than, ==equal")
    else:
        Va = sys.argv[1];
        Vb = sys.argv[2];
        compareV(Va, Vb);
