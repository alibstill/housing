# Scripts

## Price Paid script
There is a script in the root of this folder called `get_price_paid.py` that will download files from a url and save them to a `temp` folder.

You can run this from this folder:

```bash
source .venv/bin/activate

python3 ./get_price_paid.py --file_name={file_name} --base_url={base_url}
# Example
python3 ./src/get_price_paid.py --file_name=pp-2015.csv --base_url=http://endpoint.com
```

To find the relevant endpoint go to the UK gov's [Price Paid download pages](https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads).