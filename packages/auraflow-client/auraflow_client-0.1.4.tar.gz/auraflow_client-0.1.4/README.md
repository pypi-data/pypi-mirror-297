
# AuraFlow Client Library

The AuraFlow Client Library is a Python package designed to interact with the AuraFlow API to fetch financial data. This guide will walk you through the installation, configuration, and usage of the library.

## Installation

Install the AuraFlow Client Library using pip:

```bash
pip install auraflow_client
```
## Usage

Here is a simple example of how to use the library to post data and get a response:

### Example 1: Providing Input Data through User Input

If both `api_key` and `data` parameters are `None`, the user will be prompted to input the data:

```python
from auraflow_client import get_data

# Execute the function without parameters
data, status_code = get_data()
print(data, status_code)
```

When prompted, enter the data in the following format (Please follow the format strictly):
```
Enter data: {'API_KEY': 'your_api_key_here', 'data': {'ticker_list': ['^GSPC'], 'start': '2020-01-01', 'end': '2023-01-01', 'source': 'yahoo', 'data_format': 'json'}}
```

### Example 2: Passing Data through Parameters

#### Configuration

Before using the library, you need to set up your AuraFlow API key. You can do this by setting an environment variable:

```bash
export AURAFLOW_API_KEY='your_api_key_here'
```
OR
You can directly pass the `api_key` and `data` as parameters:

```python
from auraflow_client import get_api_key, get_data

# Ensure your API key is configured as per the Configuration section
api_key = get_api_key()  # or use your own method to provide the API key

# Define your parameters to send in the POST request
data = {
    'ticker_list': ['^GSPC'],       # List of tickers to retrieve data for
    "start": '2020-01-01',          # Start date for data retrieval in any format
    "end": '2023-01-01',            # End date for data retrieval in any format
    "source": 'yahoo',              # String specifying the data source. This should match the data provider you have linked with your account on the AuraFlow web portal. Valid options depend on the providers you have configured and authorized.
    "data_format": 'json'           # Format of the data returned, options are 'json' and 'csv' only
}

# Execute the function with parameters
response_data, status_code = get_data(api_key, data)
print(response_data, status_code)
```

## Environment Variables

- `AURAFLOW_API_KEY`: Set this environment variable with your AuraFlow API key to avoid passing it explicitly in your code.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any issues or inquiries, please contact our support team at support@auraflow.com.
