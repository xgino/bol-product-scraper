from datetime import datetime
import pandas as pd

date = datetime.today().strftime('%d%m-%y')

def clear_garbage(search_name):
        
    df = pd.read_csv('scraped_product.csv')

    df.drop_duplicates(subset=['title'], keep='first', inplace=True)



    # If rated lower that 7 delete row
    df['rated'] = df['rated'].fillna(0)
    df.drop(df[df.rated < 5].index, inplace=True)
    df['rated'] = pd.to_numeric(df['rated'], downcast="integer")

    #if rating lower 3.5 drop row
    df['rating'] = df['rating'].fillna(0)
    df.drop(df[df.rated < 3.2].index, inplace=True)

    # Del - in scraped price
    df['price'] = df['price'].str.replace('-','')

    # Save file, no index
    df.to_csv(f'{search_name}-{date}.csv', index=False,)


    