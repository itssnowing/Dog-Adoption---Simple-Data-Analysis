import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df, *args, **kwargs):

    table = pa.Table.from_pandas(df)
    gcs = pa.fs.GcsFileSystem()

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = 'YOUR_BUCKET_MADE_BY_TERRAFORM'
    object_key = 'petfinder_dogs'
    root_path = '{}/{}'.format(bucket_name, object_key)

    pq.write_to_dataset(
        table,
        root_path=root_path,
        filesystem=gcs,
        partition_cols=['CALC_Year', 'CALC_Month']
    )
    
