# config.py
import os


class config:
    """Centralized configuration management."""
    collection_bucket = os.environ.get("COLLECTION_BUCKET", "local-collection-data")
    issues_base_path = os.environ.get("ISSUES_BASE_PATH", 'log/issue')
    use_aws_credential_chain = os.environ.get("USE_AWS_CREDENTIAL_CHAIN", 'true').lower() == "true"
