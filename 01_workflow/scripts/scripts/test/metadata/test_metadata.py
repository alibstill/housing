import pytest
from src.metadata import Metadata


@pytest.fixture
def metadata():
    return Metadata(
        title="EPC",
        creator="Ministry of Housing",
        source="http://housingministry.com/epc",
        columns={
            "id": {"type": "str", "description": "Unique identifier"},
            "address": {"type": "str", "description": "The property address"},
            "epc_rating": {
                "type": "str",
                "description": "The epc rating for the property",
            },
        },
    )


class TestMetadata:
    def test_should_return_column_names(self, metadata: Metadata) -> None:
        expected = ["id", "address", "epc_rating"]

        assert metadata.get_column_names() == expected

    def test_should_get_summary(self, metadata: Metadata) -> None:
        expected = {
            "title": "EPC",
            "creator": "Ministry of Housing",
            "source": "http://housingministry.com/epc",
            "columns": ["id", "address", "epc_rating"],
        }

        assert metadata.get_summary() == expected
