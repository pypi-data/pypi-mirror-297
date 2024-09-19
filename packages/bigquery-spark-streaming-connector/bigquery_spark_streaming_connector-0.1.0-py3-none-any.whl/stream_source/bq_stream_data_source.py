from pyspark.sql.datasource import DataSource
from pyspark.sql.types import StructType
from google.cloud import bigquery
from stream_source.bq_stream_reader import BQStreamReader

class BQStreamDataSource(DataSource):
    """
    An example data source for streaming data from a public API containing users' comments.
    """

    @classmethod
    def name(cls):
        return "bigquery-streaming"

    def schema(self):
        type_map = {'integer': 'long', 'float': 'double'}
        client = bigquery.Client.from_service_account_json('/home/fe-dev-sandbox-a017f6995ca4.json')
        dataset_ref = client.dataset(self.options.get("dataset"), project=self.options.get("project_id"))
        table_ref = dataset_ref.table(self.options.get("table"))
        table = client.get_table(table_ref)
        original_schema = table.schema
        result = ["{0} {1}".format(schema.name, type_map.get(schema.field_type.lower(), schema.field_type.lower())) for
                  schema in table.schema]
        return ",".join(result)
        # return "census_tract double,clearance_date string,clearance_status string"

    def streamReader(self, schema: StructType):
        return BQStreamReader(schema, self.options)