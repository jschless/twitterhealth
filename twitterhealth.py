import sys
import getopt
import classifier
import twitterGUI


def main(argv):
    help = 'main.py [-c -t -v]\n'
    help += '-c or classifier : only runs classifier\n'
    help += '-t or twitter : runs classifier within twitter GUI\n'
    help += '-v or verbose : prints extra information'
    try:
        opts, args = getopt.getopt(
            argv, "htcv", ['twitter', 'classifier', 'verbose']
        )
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    if opts == []:
        print(help)
        sys.exit(0)
    twitter = False
    verbose = False
    clas = False
    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt in ('-t', '--twitter'):
            twitter = True
        elif opt in ('-c', '--classifier'):
            clas = True
        elif opt in ('-v', '--verbose'):
            verbose = True
    if twitter:
        win = twitterGUI.TwitWindow()
        win.CreateWindow()
    elif clas:
        clf = classifier.Classifier()
        if verbose:
            clf.run(verb=True)
        else:
            clf.run()


if __name__ == '__main__':
    main(sys.argv[1:])
