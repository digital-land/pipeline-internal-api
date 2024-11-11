import os
import duckdb
from schema import IssuesParams, Issue

collection_bucket = os.environ.get("COLLECTION_BUCKET", "local-collection-data")
issues_base_path = os.environ.get("ISSUES_BASE_PATH", 'log/issue')


def search_issues(params: IssuesParams):
    s3_uri = f"s3://{collection_bucket}/{issues_base_path}/**/*.parquet"
    # TODO: Handle dataset and resource query params specially to derive S3 URIs
    select = f"SELECT * FROM '{s3_uri}'"
    pagination = f"LIMIT {params.limit} OFFSET {params.offset}"
    where_clause = ""
    if params.field:
        where_clause += _add_condition(where_clause, f"field = '{params.field}'")
    if params.issue_type:
        where_clause += _add_condition(where_clause, f"\"issue-type\" = '{params.issue_type}'")
    sql = f"{select} {where_clause} {pagination}"
    print(sql)
    with duckdb.connect() as conn:
        return conn.execute(sql).arrow().to_pylist()


def _add_condition(where_clause, condition):
    if len(where_clause) == 0:
        conjunction = "WHERE"
    else:
        conjunction = "AND"
    return f"{conjunction} {condition} "


