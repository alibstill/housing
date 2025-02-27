# Scripts

## Create remote backend

You can use the `create_remote_backend.py` script to create a GCS bucket.

Default arguments:
- bucket_name = `f"{random_uuid}-tf-remote-backend"`
- location = "EUROPE-WEST2"

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

GOOGLE_APPLICATION_CREDENTIALS="../.credentials/tf-dev.json" python create_remote_backend.py
```

You can create a bucket in a different location with a bespoke name:

```bash
GOOGLE_APPLICATION_CREDENTIALS="../.credentials/tf-dev.json" python create_remote_backend.py --location=EU --bucket_name=unique-id-tf-remote-backend
```
