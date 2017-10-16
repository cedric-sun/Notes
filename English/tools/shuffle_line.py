from random import shuffle

def main():
    mfile = open('tmp.txt')
    lines = mfile.readlines();
    mfile.close()
    words = []
    legal_initials = [ chr(x) for x  in range(ord('a'),ord('z')+1) + range(ord('A'), ord('Z')+1)]
    for line in lines:
        stripped = line.strip()
        if stripped != "" and stripped[0] in legal_initials:
            res = '\t'.join(stripped.split('\t')[:2])
            words.append(res+'\n')
        else:
            print(stripped)
    shuffle(words)
    ofile = open('shuffled.txt','w')
    ofile.writelines(words)
    ofile.close()


if __name__ == "__main__":
    main()
