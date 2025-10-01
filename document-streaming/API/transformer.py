import numpy as np
from numpy import add
import pandas as pd


uber_df = pd.read_csv('../data/ncr_ride_bookings.csv')

#print(uber_df.head())

#print(uber_df.dtypes)

#add json column to dataframe
#split json column into multiple rows

# Remove quotes from Booking ID and Customer ID columns
uber_df['Booking ID'] = uber_df['Booking ID'].str.strip('"')
uber_df['Customer ID'] = uber_df['Customer ID'].str.strip('"')

uber_df['json'] = uber_df.to_json(orient='records', lines=True).splitlines()

#return json column as dataframe
uber_df_json = uber_df['json']

#save dataframe to text file
np.savetxt('../data/ncr_ride_bookings.txt', uber_df_json.values, fmt='%s')