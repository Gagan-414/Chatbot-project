import pandas as pd
from INSERT_INTO_SQL import Write_into_SQL
from datetime import datetime

def Get_from_CSV(csvfile):
    # Specify dtype for 'contact' column to ensure it's read as a string
    DATA = pd.read_csv(csvfile, dtype={'contact': str})
    DATA_COPY = DATA.dropna()
    length = len(DATA_COPY) - 1

    now = datetime.now()
    # date_time = now.strftime("%d/%m/%Y, %H:%M:%S")

    # Now the 'contact' column is already a string, no need to convert
    name = DATA_COPY['name'].values[length]
    email = DATA_COPY['email'].values[length]
    contact = DATA_COPY['contact'].values[length]
    query = DATA_COPY['query'].values[length]

    Write_into_SQL( name, email, contact, query)
    print('Data Write into SQL Successfully')

# Get_from_CSV("parameter_values.csv")
