import pandas as pd

def main():

    name, n, m = input().split()

    df = pd.read_csv(name, sep=';')
    
    print(df.iloc[int(n) - 1, int(m)])
main()
