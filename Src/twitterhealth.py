import sys
import getopt
import classifier
import twitterGUI
import subprocess


def main(argv):
    help = '''main.py [-t -v -f --test]\n
    -t or --twitter : runs classifier within twitter GUI\n
    -v or --verbose : prints extra information\n
    -f [folds] or --folds=[folds] : set number of folds
    for validation\n
    --test : runs test code\n
    --timing : runs timing code\n
    -m [model] or --model=[model]: sets model to be tested\n
    --results: run test with many models\n
    -e or --election: runs model and displays election interference tweets'''

    try:
        opts, args = getopt.getopt(
            argv, "htcvef:m:",
            ['twitter', 'classifier', 'verbose', 'test', 'timing', 'folds=',
                'model=', 'results', 'election']
        )
    except getopt.GetoptError:
        print(help)
        sys.exit(2)

    twitter = False
    verbose = False
    test = False
    results = False
    timing = False
    election_data = False
    model = 'MLP'
    folds = 2
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
            folds = int(arg)
        elif opt in ('--timing'):
            timing = True
        elif opt in ('-m', '--model'):
            model = arg
        elif opt in ('--results'):
            results = True
        elif opt in ('-e', '--election'):
            election_data = True
    if results:
        n = 3
        for model in ['MLP', 'SVC', 'SGD', 'NN', 'GAUS', 'TREE']:
            for trial in range(n):
                print(model + ' trial ' + str(trial+1))
                subprocess.call(['python', 'twitterhealth.py',
                                 '-f', '2', '-m', model])
    elif test:
        subprocess.call(['pytest', '..\\Test\\test_net.py'])
    else:
        clf = classifier.Classifier(folds=folds, timing=timing, model=model)
        if verbose:
            clf.run(verb=True)
        else:
            clf.run()
        if twitter:
            if election_data:
                win = twitterGUI.TwitWindow(clf, data='Election')
            else:
                win = twitterGUI.TwitWindow(clf)
            win.CreateWindow()


if __name__ == '__main__':
    main(sys.argv[1:])
