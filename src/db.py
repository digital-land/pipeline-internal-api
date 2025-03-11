import duckdb
from log import get_logger
from schema import (
    CommonParams,
    IssuesParams,
    SpecificationsParams,
    IssueTypeSummaryParams,
)
from pagination_model import PaginationParams, PaginatedResult
from config import config
import json

logger = get_logger(__name__)


def search_issues(params: IssuesParams):
    s3_uri = f"s3://{config.collection_bucket}/{config.issues_base_path}/**/*.parquet"  # noqa

    where_clause = ""
    query_params = []

    if params.dataset:
        where_clause += _add_condition(where_clause, "dataset = ?")
        query_params.append(params.dataset)
    if params.resource:
        where_clause += _add_condition(where_clause, "resource = ?")
        query_params.append(params.resource)
    if params.field:
        where_clause += _add_condition(where_clause, "field = ?")
        query_params.append(params.field)
    if params.issue_type:
        where_clause += _add_condition(where_clause, "issue-type = ?")
        query_params.append(params.issue_type)

    sql_count = f"SELECT COUNT(*) FROM '{s3_uri}' {where_clause}"
    logger.debug(sql_count)
    sql_results = f"SELECT * FROM '{s3_uri}' {where_clause} LIMIT ? OFFSET ?"
    logger.debug(sql_results)

    return duck_db_connection(params, query_params, sql_count, sql_results)


def search_provision_summary(params: CommonParams):
    s3_uri = f"s3://{config.collection_bucket}/{config.performance_base_path}/provision_summary.parquet"  # noqa

    where_clause = ""
    query_params = []

    if params.dataset:
        where_clause += _add_condition(where_clause, "dataset = ?")
        query_params.append(params.dataset)

    if params.organisation:
        where_clause += _add_condition(where_clause, "organisation = ?")
        query_params.append(params.organisation)

    sql_count = f"SELECT COUNT(*) FROM '{s3_uri}' {where_clause}"
    sql_results = f"SELECT * FROM '{s3_uri}' {where_clause} LIMIT ? OFFSET ?"

    logger.debug(sql_count)
    logger.debug(sql_results)

    return duck_db_connection(params, query_params, sql_count, sql_results)


def search_issue_type_summary(params: IssueTypeSummaryParams):
    s3_uri = f"s3://{config.collection_bucket}/{config.performance_base_path}/endpoint_dataset_issue_type_summary.parquet"  # noqa

    where_clause = ""
    query_params = []

    if params.dataset:
        where_clause += _add_condition(where_clause, "dataset = ?")
        query_params.append(params.dataset)

    if params.organisation:
        where_clause += _add_condition(where_clause, "organisation = ?")
        query_params.append(params.organisation)

    if params.issueType:
        where_clause += _add_condition(where_clause, "issue_type = ?")
        query_params.append(params.issueType)

    if params.issueField:
        where_clause += _add_condition(where_clause, "issue_field = ?")
        query_params.append(params.issueField)

    if params.severity:
        where_clause += _add_condition(where_clause, "severity = ?")
        query_params.append(params.severity)

    if params.responsibility:
        where_clause += _add_condition(where_clause, "responsibility = ?")
        query_params.append(params.responsibility)

    sql_count = f"SELECT COUNT(*) FROM '{s3_uri}' {where_clause}"
    sql_results = f"""
    SELECT organisation, organisation_name, dataset, resource, issue_type, field, 
count_issues, severity, responsibility  FROM '{s3_uri}' {where_clause} LIMIT ? OFFSET ?"""

    logger.debug(sql_count)
    logger.debug(sql_results)

    return duck_db_connection(params, query_params, sql_count, sql_results)


def search_dataset_resource_mapping(params: CommonParams):
    s3_uri = f"s3://{config.collection_bucket}/{config.performance_base_path}/endpoint_dataset_resource_summary.parquet"  # noqa

    where_clause = ""
    query_params = []

    if params.dataset:
        where_clause += _add_condition(where_clause, "dataset = ?")
        query_params.append(params.dataset)

    if params.organisation:
        where_clause += _add_condition(where_clause, "organisation = ?")
        query_params.append(params.organisation)

    sql_count = f"SELECT COUNT(*) FROM '{s3_uri}' {where_clause}"
    sql_results = f"SELECT * FROM '{s3_uri}' {where_clause} LIMIT ? OFFSET ?"

    logger.debug(sql_count)
    logger.debug(sql_results)

    return duck_db_connection(params, query_params, sql_count, sql_results)


def search_endpoint_dataset_summary(params: CommonParams):
    s3_uri = f"s3://{config.collection_bucket}/{config.performance_base_path}/endpoint_dataset_summary.parquet"  # noqa

    where_clause = ""
    query_params = []

    if params.dataset:
        where_clause += _add_condition(where_clause, "dataset = ?")
        query_params.append(params.dataset)

    if params.organisation:
        where_clause += _add_condition(where_clause, "organisation = ?")
        query_params.append(params.organisation)

    sql_count = f"SELECT COUNT(*) FROM '{s3_uri}' {where_clause}"
    sql_results = f"SELECT * FROM '{s3_uri}' {where_clause} LIMIT ? OFFSET ?"

    logger.debug(sql_count)
    logger.debug(sql_results)

    return duck_db_connection(params, query_params, sql_count, sql_results)


def get_specification(params: SpecificationsParams):
    s3_uri = f"s3://{config.collection_bucket}/{config.specification_base_path}/*.parquet"  # noqa

    where_clause = ""
    query_params = {}

    if params.dataset:
        where_clause += _add_condition(
            where_clause,
            "TRIM(BOTH '\"' FROM json_extract(json(value), '$.dataset')) = ?",
        )
        query_params["dataset"] = params.dataset

    sql_count = f"""
    SELECT COUNT(*) FROM (
    SELECT unnest(CAST(json AS VARCHAR[])) AS value 
    FROM '{s3_uri}') AS parsed_json {where_clause}
    LIMIT ? OFFSET ?
    """

    sql_results = f"""
    SELECT value AS json FROM (
    SELECT unnest(CAST(json AS VARCHAR[])) AS value 
    FROM '{s3_uri}') AS parsed_json {where_clause} 
    LIMIT ? OFFSET ?
    """

    logger.debug(sql_count)
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

            # Execute queries with parameters
            count = conn.execute(
                sql_count, [*query_params.values(), params.limit, params.offset]
            ).fetchone()[0]
            results = (
                conn.execute(
                    sql_results, [*query_params.values(), params.limit, params.offset]
                )
                .arrow()
                .to_pylist()
            )

            # Convert JSON strings to actual JSON objects
            json_results = []
            for item in results:
                if "json" in item and isinstance(item["json"], str):
                    try:
                        parsed_json = json.loads(item["json"])
                        json_results.append(parsed_json)
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON format in row: {item['json']}")

            return PaginatedResult(
                params=PaginationParams(offset=params.offset, limit=params.limit),
                total_results_available=count,
                data=json_results,
            )
        except Exception as e:
            logger.exception("Failure executing DuckDB queries")
            raise e


def _add_condition(where_clause, condition):
    if len(where_clause) == 0:
        conjunction = "WHERE"
    else:
        conjunction = "AND"
    return f"{conjunction} {condition} "


def duck_db_connection(params, query_params, sql_count, sql_results):
    with duckdb.connect() as conn:
        try:
            if config.use_aws_credential_chain:
                logger.debug(
                    conn.execute(
                        "CREATE SECRET aws (TYPE S3, PROVIDER CREDENTIAL_CHAIN);"
                    ).fetchall()
                )
                logger.debug(conn.execute("FROM duckdb_secrets();").fetchall())

            # Execute parameterized queries
            count = conn.execute(sql_count, query_params).fetchone()[0]
            results = (
                conn.execute(sql_results, query_params + [params.limit, params.offset])
                .arrow()
                .to_pylist()
            )

            return PaginatedResult(
                params=PaginationParams(offset=params.offset, limit=params.limit),
                total_results_available=count,
                data=results,
            )
        except Exception as e:
            logger.exception("Failure executing DuckDB queries")
            raise e
