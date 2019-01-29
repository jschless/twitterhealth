import pandas as pd
from tweet import *

def main():
    path = "C:\\Users\\EECS\\Documents\\ElectionInterference\\" #\\ira_tweets_csv_hashed.csv"

    df1 = pd.read_csv(path + "ira_tweets_csv_hashed.csv")
    df2 = pd.read_csv(path + "iranian_tweets_csv_hashed.csv")

    return pd.concat([df1,df2])

temp = main()
print(temp.head())
