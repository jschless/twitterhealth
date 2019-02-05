import csv
with open('C:\\Users\\EECS\\Documents\\cred_event_TurkRatings.data') as f:
    next(f) # skip headings
    reader=csv.reader(f,delimiter='\t')
    for key, terms, ratings, reasons in reader:
        print(reasons)
