# appwise-legacy-events-loadtest
Legacy event generator for load testing


## Dependencies
- python3

## Installation

Clone the repo.

```
cd appwise-legacy-events-loadtest
pip install -r requirements.txt
```

## Configuration

Follow the guide [here](http://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html) to set up AWS client credentials

## Usage

Running
```
python load_test -n 1000 -t 8 -q legacy-connector-events-dev
```
will generate 1000 events, submitted in batches of 10 by 8 threads to the `legacy-connector-events-dev` queue.

