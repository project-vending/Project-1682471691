python
import streamlit as st
import boto3
import pandas as pd

# create connection to s3 bucket
s3 = boto3.resource('s3')
bucket_name = '<insert your bucket name here>'
bucket = s3.Bucket(bucket_name)

# specify the key for the data file in your s3 bucket
key = '<insert key to your file in S3>'

# create a dataframe from the data file in S3
obj = bucket.Object(key).get()
df = pd.read_csv(obj['Body'])

def main():
    st.title('E-commerce Data Pipeline')

    st.header('Transaction Data')

    # display the dataframe in a table
    st.dataframe(df)

if __name__ == '__main__':
    main()
