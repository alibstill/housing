# Scripts

## Setting up the virtual environment

There is a `requirements.txt` file you can use to create a local virtual environment:

```bash
# pip install virtualenv # if you don't have virtualenv already

# create new environment
virtualenv .venv 

# load venv
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

## Price Paid script
There is a script in the root of this folder called `get_price_paid.py`. 

If run locally, it will download files from a url and save them to a `temp` folder.

For an overview of the inputs, use the help function:

```bash
cd scripts
source .venv/bin/activate
python ./get_price_paid.py --help
```

You can run this from this folder:

```bash
cd scripts
source .venv/bin/activate

python ./get_price_paid.py --file_name={file_name} --base_url={base_url}
# Example
python ./get_price_paid.py --file_name=pp-2015.csv --base_url=http://endpoint.com
```

To find the relevant endpoint go to the UK gov's [Price Paid download pages](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads).

## Process CSV script

This script adds a location hash column to the price paid dataset and converts it to parquet.

If run locally this script will process a specific csv file in the `src/temp` folder.

For an overview of the inputs, use the help function:

```bash
cd scripts
source .venv/bin/activate
python process_csv.py --help
```

You can run this from this folder:

```bash
python process_csv.py --src_file_name={src_file_name} 

# Example
python process_csv.py --src_file_name=pp-2015 
```

## Testing, Linting and Coverage

1. Testing

The scripts are unit tested with `pytest`:

```bash
cd scripts
source .venv/bin/activate
pytest . -v
```

2. Coverage

Run the tests with coverage:

```bash
coverage run -m pytest .
coverage report
```

3. Ruff 

To run the linter:

```bash
cd scripts
source .venv/bin/activate
ruff check . 
ruff check --fix 
```

To format files run: 

```bash
cd scripts
source .venv/bin/activate
ruff format . 
```



