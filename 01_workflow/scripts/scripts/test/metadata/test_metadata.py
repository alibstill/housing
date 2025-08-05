import pytest
from unittest import TestCase
from src.metadata import Metadata, metadata_mapper
from src.metadata import price_paid


class TestMetadata(TestCase):

    def setUp(self):
        self.metadata = Metadata(
            title="EPC",
            creator="Ministry of Housing",
            source="http://housingministry.com/epc",
            columns={
                "id": {"type": "int", "description": "Unique identifier"},
                "address": {"type": "string", "description": "The property address"},
                "epc_rating": {
                    "type": "string",
                    "description": "The epc rating for the property",
                },
            },
        )

    def test_should_return_column_names(self) -> None:
        expected = ["id", "address", "epc_rating"]

        self.assertEqual(self.metadata.get_column_names(), expected)

    def test_should_get_summary(self) -> None:
        expected = {
            "title": "EPC",
            "creator": "Ministry of Housing",
            "source": "http://housingministry.com/epc",
            "columns": ["id", "address", "epc_rating"],
        }

        self.assertEqual(self.metadata.get_summary(), expected)

    def test_should_get_dtypes_map(self) -> None:
        expected = {"id": "int", "address": "string", "epc_rating": "string"}
        self.assertEqual(self.metadata.get_column_dtypes(), expected)

    def test_price_paid_metadata_types(self) -> None:
        expected = {
            "county": "string",
            "date_of_transfer": "string",
            "district": "string",
            "is_new_build": "string",
            "locality": "string",
            "paon": "string",
            "postcode": "string",
            "price": "int",
            "property_type": "string",
            "record_status": "string",
            "saon": "string",
            "street": "string",
            "tenure_duration": "string",
            "town_city": "string",
            "transaction_type": "string",
            "transaction_uid": "string",
        }
        price_paid_meta = metadata_mapper.get("price_paid")
        dtypes = price_paid_meta.get_column_dtypes()

        self.assertEqual(dtypes, expected)
