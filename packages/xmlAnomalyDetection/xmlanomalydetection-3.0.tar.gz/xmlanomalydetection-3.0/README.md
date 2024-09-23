# Introduction

This repo. serves to develop the strategy to assess whether user has entered anomalous value while
filling the expenses. 

It assumes xml that will be exported from BPM solution and extracts meaning ful data from it, later uses 
language model to assess and detect anomalies.




# Build the project and run server

Following will build the project binaries so that it could be installed via `pip`  

ist create a `.env` file with key `GROQ_API_KEY` , (get the free api key from [groq server](groq.com))


```bash

python setup.py bdist_wheel
python setup.py sdist 

```
This will create some binaries in dist and build folders, install it as package like:

```bash
cd dist
pip install xmlAnomalyDetection-2.0-py3-none-any.whl
```


## Run server

Once the project is built , run following in the terminal, it will run the server:
```bash
xml_anomaly_detection
```


# Run without building

Binaries are already pushed to pypi, do following to just pull them and install them:

```bash

pip install xmlAnomalyDetection==2.0
```

Then run following in the terminal, it will run the server:
```bash
xml_anomaly_detection
```


# Test request

```curl
curl -X 'POST' \
  'http://0.0.0.0:8357/detect_anomaly' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'xml_file=@xml_sample.xml;type=text/xml'

```

It will return response like:

```bash
[
  {
    "user_entered_values": [
      "2022-11-08",
      "Travel | Car Rental",
      "200",
      "21"
    ],
    "entered_values_decriptions": [
      "Date of expense",
      "Type of expense",
      "Expense amount",
      "Brief description"
    ],
    "is_anomaly": "False",
    "reason": []
  },
  {
    "user_entered_values": [
      "2022-11-08",
      "Transportation | Fuel",
      "200",
      "212"
    ],
    "entered_values_decriptions": [
      "Date of expense",
      "Type of expense",
      "Expense amount",
      "Brief description"
    ],
    "is_anomaly": "False",
    "reason": []
  }
]

```

If `is_anomaly` is  `True` in any of the returned records, it means there is anomaly. Rest of the items in record are metadata. 