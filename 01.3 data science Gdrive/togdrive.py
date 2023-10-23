
#load the data into a dataframe
import datetime, time
import pandas as pd
import pydrive 
from google.cloud import storage

tinker = 'TSLA'
#here you can select time period
period1 = int(time.mktime(datetime.datetime(2019, 7, 1, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2019, 7, 31, 23, 59).timetuple()))
interval = '1d' # 1wk, 1m
#file location
query_string = f'insert file location'  

df = pd.read_csv(query_string)
print(df)

#input gcloud auth application-default login to login in vs/anyprogram to use gdrive with commands below
#dataframe table to cloud storage
client = storage.Client('insert location here') #google key/google json file location on pc
export_bucket = client.get_bucket('insert correct name from gdrive') #correct google bucket

df.to_csv()

#bucket.blob(file_name).upload()
type(export_bucket.blob('tsla {0}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S'))))
export_bucket.blob('tsla {0}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S'))).upload_from_string(df.to_csv(), 'text/csv')

