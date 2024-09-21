import os
import pandas as pd
from django.conf import settings


class DFDataMixin:
    """A class to store data in a DataFrame. It enables to create dataframes and export them to CSV files."""

    @classmethod
    def get_dataframe(cls) -> pd.DataFrame:
        """Creates a DataFrame from the data stored in the database table."""
        columns = [field.name for field in cls._meta.fields]
        data = list(cls.objects.values_list(*columns))
        df = pd.DataFrame(data, columns=columns)
        return df

    @classmethod
    def export_to_csv(cls):
        """Exports the data stored in the database table to a CSV file."""
        table_name = cls._meta.db_table
        print(f"Exporting {table_name} to CSV file...")
        df = cls.get_dataframe()
        destination_path = os.path.join(settings.ANALYTICS_DATA_DIR, f"{table_name}.csv")
        df.to_csv(destination_path, index=True)
        print(f"{table_name.capitalize()} exported to {destination_path}")
