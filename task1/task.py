import pandas as pd

class main():

    name, n, m = input().split()

    df = pd.read_csv(name, sep=';')

    print()
    print(df.iloc[int(n) - 1, int(m)])
main()