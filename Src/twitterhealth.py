import sys
import getopt
import classifier
import twitterGUI
import subprocess

def main(argv):
    help = 'main.py [-t -v -f --test]\n'
    help += '-t or --twitter : runs classifier within twitter GUI\n'
    help += '-v or --verbose : prints extra information\n'
    help += '-f [folds] or --folds=[folds] : set number of folds '
    help += 'for validation\n'
    help += '--test : runs test code [TODO]\n'
    try:
        opts, args = getopt.getopt(
            argv, "htcvf:",
            ['twitter', 'classifier', 'verbose', 'test', 'folds=']
        )
    except getopt.GetoptError:
        print(help)
        sys.exit(2)

    twitter = False
    verbose = False
    test = False
    folds = 5
    for opt, arg in opts:
        if opt == '-h':
            print(help)
            sys.exit()
        elif opt in ('-t', '--twitter'):
            twitter = True
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('--test'):
            test = True
        elif opt in ('-f', '--folds'):
            folds = arg

    if test:
        subprocess.call(['pytest', '..\\Test\\test_net.py'])
    else:
        clf = classifier.Classifier(folds=folds)
        if verbose:
            clf.run(verb=True)
        else:
            clf.run()
        if twitter:
            win = twitterGUI.TwitWindow(clf)
            win.CreateWindow()


if __name__ == '__main__':
    main(sys.argv[1:])
