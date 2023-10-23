
#step 1 load the data into a dataframe
import datetime, time
import pandas as pd
import pydrive 
from google.cloud import storage

tinker = 'TSLA'
period1 = int(time.mktime(datetime.datetime(2019, 7, 1, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2019, 7, 31, 23, 59).timetuple()))
interval = '1d' # 1wk, 1m
query_string = f'C:/Users/hnrf/OneDrive/Документы/a CODE/01.2 data science analysis/TSLA.csv'

df = pd.read_csv(query_string)
print(df)

#input gcloud auth application-default login to login in vs/anyprogram to use gdrive with commands below
#step 2 upload dataframe table to cloud storage
client = storage.Client('C:/Users/hnrf/OneDrive/Документы/a CODE/01.3 data science Gdrive/client_secret_939665611566-niagp7rk4s4noc7undmuo6ejscaj2qhk.apps.googleusercontent.com.json')
export_bucket = client.get_bucket('myd-storage-bucketmyd-storage-bucket') 

df.to_csv()

#bucket.blob(file_name).upload()
type(export_bucket.blob('tsla {0}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S'))))
export_bucket.blob('tsla {0}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S'))).upload_from_string(df.to_csv(), 'text/csv')

