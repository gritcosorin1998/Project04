import requests
import json
import pandas as pd
import numpy as np


if __name__ == "__main__":

    excel_file = "db_extracted_text.xlsx"
    df = pd.read_excel(excel_file)
    df['id'] = df.index
    df['sentiment'] = np.nan
    df['sentiment_weight'] = 0.00
    print(df.head())

    # Iterate through the "example" column
    for index, value in enumerate(df['link']):
        print(f"Row {index + 1}: {value}")


        # Define the URL
        url = 'http://localhost:8989/rest/process'

        # Define the payload data
        payload = [
            {
                "content": value,
                "language": "EMPTY"
            }
        ]

        # Convert the payload to JSON
        json_payload = json.dumps(payload)

        # Define headers
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        # Make the POST request
        response = requests.post(url, headers=headers, data=json_payload)
        # Check if the request was successful
        if response.status_code == 200:
            print("Request successful")
            print("Response:", response.json())
            print(response.json()[0]['text'])
            df.at[index, 'extracted_text'] = response.json()[0]['text']
        else:
            print("Request failed with status code:", response.status_code)

    df.to_csv('db_extracted_text.xlsx', index=False)
