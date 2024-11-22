import os
import duckdb
from log import get_logger
from schema import IssuesParams
from pagination_model import PaginationParams, PaginatedResult

collection_bucket = os.environ.get("COLLECTION_BUCKET", "local-collection-data")
issues_base_path = os.environ.get("ISSUES_BASE_PATH", 'log/issue')

logger = get_logger(__name__)


def search_issues(params: IssuesParams):
    s3_uri = f"s3://{collection_bucket}/{issues_base_path}/**/*.parquet"
    pagination = f"LIMIT {params.limit} OFFSET {params.offset}"

    where_clause = ""
    if params.dataset:
        where_clause += _add_condition(where_clause, f"dataset = '{params.dataset}'")
    if params.resource:
        where_clause += _add_condition(where_clause, f"resource = '{params.resource}'")
    if params.field:
        where_clause += _add_condition(where_clause, f"field = '{params.field}'")
    if params.issue_type:
        where_clause += _add_condition(where_clause, f"\"issue-type\" = '{params.issue_type}'")

    sql_count = f"SELECT COUNT(*) FROM '{s3_uri}' {where_clause}"
    logger.debug(sql_count)
    sql_results = f"SELECT * FROM '{s3_uri}' {where_clause} {pagination}"
    logger.debug(sql_results)

    with duckdb.connect() as conn:
        try:
            logger.info(conn.execute("FROM duckdb_secrets();").fetchall())
            count = conn.execute(sql_count).fetchone()[0]  # Count is first item in Tuple
            logger.debug(count)
            results = conn.execute(sql_results).arrow().to_pylist()
            return PaginatedResult(
                params=PaginationParams(offset=params.offset, limit=params.limit),
                total_results_available=count,
                data=results
            )
        except Exception as e:
            logger.exception(
                "Failure executing DuckDB queries",
            )
            raise e


def _add_condition(where_clause, condition):
    if len(where_clause) == 0:
        conjunction = "WHERE"
    else:
        conjunction = "AND"
    return f"{conjunction} {condition} "


