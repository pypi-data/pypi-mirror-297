# markets_analytics

 A utility [package](https://test.pypi.org/project/markets-analytics/) to that helps with data analytics by reducing boiler plate code and replacing them with helper function for database interactivity, ETL pipelines, Google Sheets, and dates.

## Installation

```sh
pip install markets_analytics 
```

# Imports

The following examples showcase how to import packages for the areas you're interested in.

Although you can import original classes like `RedshiftConnector`, aliases have already been provided to reduce this step further.

Database connectivity:

```python
from markets_analytics import redshift, datalake, exasol
```

ETL pipelines:

```python
from markets_analytics import etl
```

Google Sheets:

```python
from markets_analytics import GSheetHelper
gsheet = GSheetHelper('<Name of the GSheet>')
```

Date utilities:

```python
from markets_analytics import dateutil
```

Google Chat:

```python
from markets_analytics import GoogleChat
gchat = GoogleChat('<Webhook URL of the Google Chat Space>')
```

Email

```python
from markets_analytics import Email
email = Email('<Your Email ID>', '<Your Email App Password>') # App Password is setup via Google 2FA Security tab
```

## Releasing New Version

To release new versions after making changes, we need to update the `pyproject.toml` file and increment the version's minor or major counter by 1. You would then be able to run the following in your terminal (make sure dist only contains the new version files after build command has successfully completed):

```
python3 -m pip install --upgrade build twine
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```