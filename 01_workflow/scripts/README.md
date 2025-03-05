# Scripts

## Price Paid script
There is a script in the root of this folder called `get_price_paid.py`. 

If run locally, it will download files from a url and save them to a `temp` folder.

For an overview of the inputs, use the help function:

```bash
sourc .venv/bin/activate
python ./get_price_paid.py --help
```

You can run this from this folder:

```bash
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
source .venv/bin/activate
python process_csv.py --help
```

You can run this from this folder:

```bash
python process_csv.py --src_file_name={src_file_name} 

# Example
python process_csv.py --src_file_name=pp-2015 
```

## CSV to pq script

This script converts a csv file to parquet. 

If run locally this script will convert a specific csv file in the `src/temp` folder to parquet.

For an overview of the inputs, use the help function:

```bash
sourc .venv/bin/activate
python csv_to_pq.py --help
```

You can run this from this folder:

```bash
python csv_to_pq.py --src_file_name={src_file_name} 

# Example
python csv_to_pq.py --src_file_name=pp-2015 
```