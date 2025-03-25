class Metadata:
    def __init__(self, title: str, creator: str, source: str, columns: dict) -> None:
        self.title = title
        self.creator = creator
        self.source = source
        self.columns = columns

    def add_column(self, column_name: str, column_type: str, description: str):
        self.columns[column_name] = {"type": column_type, "description": description}

    def get_column_names(self) -> list:
        return list(self.columns.keys())

    def get_summary(self) -> dict:
        return {
            "title": self.title,
            "creator": self.creator,
            "source": self.source,
            "columns": list(self.columns.keys()),
        }
