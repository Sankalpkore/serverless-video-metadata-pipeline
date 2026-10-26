import urllib.parse
from datetime import datetime, timezone

import boto3

s3 = boto3.client("s3")
table = boto3.resource("dynamodb").Table("videos")


def lambda_handler(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])

        head = s3.head_object(Bucket=bucket, Key=key)

        table.put_item(Item={
            "object_key": key,
            "bucket": bucket,
            "size_bytes": head["ContentLength"],
            "content_type": head["ContentType"],
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        })
    return {"statusCode": 200}
