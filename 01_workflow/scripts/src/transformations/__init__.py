from .price_paid_transformer import PricePaidTransformer
from typing import Protocol
import pandas as pd
from logging import Logger

transformations_mapper = {"price_paid": PricePaidTransformer}


class Transformer(Protocol):
    def apply(df: pd.DataFrame, logger: Logger) -> pd.DataFrame: ...


__all__ = ["PricePaidTransformer", "transformations_mapper"]
