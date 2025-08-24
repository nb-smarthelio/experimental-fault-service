import awswrangler as wr
import boto3

from heliolib.data_extraction_service import TimestreamDataExtractor
from heliolib.metadata_extraction_service import MetadataAPI

aws_timestream_client = wr.timestream
metadata_api_object = MetadataAPI()
boto3_session = boto3.Session(aws_access_key_id="your_access_key",
                              aws_secret_access_key="your_secret_key",
                              region_name="your_region")
timestream_extractor = TimestreamDataExtractor(aws_timestream_client=aws_timestream_client,
                                               metadata_api_object=metadata_api_object
                                               )

