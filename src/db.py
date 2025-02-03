import duckdb
from log import get_logger
from schema import IssuesParams, ProvisionParams
from pagination_model import PaginationParams, PaginatedResult
from config import config


logger = get_logger(__name__)

def search_issues(params: IssuesParams):
    s3_uri = f"s3://{config.collection_bucket}/{config.issues_base_path}/**/*.parquet"
    pagination = f"LIMIT {params.limit} OFFSET {params.offset}"

    where_clause = ""
    if params.dataset:
        where_clause += _add_condition(where_clause, f"dataset = '{params.dataset}'")
    if params.resource:
        where_clause += _add_condition(where_clause, f"resource = '{params.resource}'")
    if params.field:
        where_clause += _add_condition(where_clause, f"field = '{params.field}'")
    if params.issue_type:
        where_clause += _add_condition(
            where_clause, f"\"issue-type\" = '{params.issue_type}'"
        )

    sql_count = f"SELECT COUNT(*) FROM '{s3_uri}' {where_clause}"
    logger.debug(sql_count)
    sql_results = f"SELECT * FROM '{s3_uri}' {where_clause} {pagination}"
    logger.debug(sql_results)

    with duckdb.connect() as conn:
        try:
            if config.use_aws_credential_chain:
                logger.debug(
                    conn.execute(
                        "CREATE SECRET aws (TYPE S3, PROVIDER CREDENTIAL_CHAIN);"
                    ).fetchall()
                )
                logger.debug(conn.execute("FROM duckdb_secrets();").fetchall())
            count = conn.execute(sql_count).fetchone()[
                0
            ]  # Count is first item in Tuple
            results = conn.execute(sql_results).arrow().to_pylist()
            return PaginatedResult(
                params=PaginationParams(offset=params.offset, limit=params.limit),
                total_results_available=count,
                data=results,
            )
        except Exception as e:
            logger.exception(
                "Failure executing DuckDB queries",
            )
            raise e

def search_provision_summary(params: ProvisionParams):
    s3_uri = f"s3://{config.collection_bucket}/{config.performance_base_path}/*.parquet"
    pagination = f"LIMIT {params.limit} OFFSET {params.offset}"

    where_clause = ""
    if params.dataset:
        where_clause += _add_condition(where_clause, f"dataset = '{params.dataset}'")
    if params.organisation:
        where_clause += _add_condition(where_clause, f"organisation = '{params.organisation}'")
   
    sql_count = f"SELECT COUNT(*) FROM '{s3_uri}' {where_clause}"
    logger.debug(sql_count)
    sql_results = f"SELECT * FROM '{s3_uri}' {where_clause} {pagination}"
    logger.debug(sql_results)

    with duckdb.connect() as conn:
        try:
            if config.use_aws_credential_chain:
                logger.debug(
                    conn.execute(
                        "CREATE SECRET aws (TYPE S3, PROVIDER CREDENTIAL_CHAIN);"
                    ).fetchall()
                )
                logger.debug(conn.execute("FROM duckdb_secrets();").fetchall())
            count = conn.execute(sql_count).fetchone()[
                0
            ]  # Count is first item in Tuple
            results = conn.execute(sql_results).arrow().to_pylist()
            return PaginatedResult(
                params=PaginationParams(offset=params.offset, limit=params.limit),
                total_results_available=count,
                data=results,
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
