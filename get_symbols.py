
import pandas as pd 
def Main():
        df=pd.read_csv('/var/www/vectorspace.ai/html/viz/data/dataset.tsv', index_col=0, delimiter="$
        print(df.axes[0].tolist())
if __name__ == '__main__':
        Main()











