import duckdb
import sys

s3_uri = sys.argv[1] if len(sys.argv) > 1 else "s3://production-collection-data/data/performance/endpoint_dataset_issue_type_summary.parquet"

with duckdb.connect() as conn:
    conn.execute("CREATE SECRET aws (TYPE S3, PROVIDER CREDENTIAL_CHAIN);")
    print(conn.execute(f"DESCRIBE SELECT * FROM '{s3_uri}'").df().to_string())
    print()
    print(conn.execute(f"SELECT * FROM '{s3_uri}' LIMIT 10").df().to_string())
