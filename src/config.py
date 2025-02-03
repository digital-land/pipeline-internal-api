# config.py
import os


class config:
    """Centralized configuration management."""

    collection_bucket = os.environ.get("COLLECTION_BUCKET", "local-collection-data")
    issues_base_path = os.environ.get("ISSUES_BASE_PATH", "log/issue")
    performance_base_path = os.environ.get("PERFORMANCE_BASE_PATH", "data/performance")
    specification_base_path = os.environ.get("SPECIFICATION_BASE_PATH", "data/specification")
    use_aws_credential_chain = (
        os.environ.get("USE_AWS_CREDENTIAL_CHAIN", "true").lower() == "true"
    )

