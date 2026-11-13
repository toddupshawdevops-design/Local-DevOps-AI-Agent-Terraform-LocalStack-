import os
import boto3
from dotenv import load_dotenv

load_dotenv()

# Set to True for LocalStack emulation (:4566), False for live AWS
USE_LOCAL_AWS = os.getenv("USE_LOCAL_AWS", "True").lower() == "true"

ENDPOINT_URL = "http://127.0.0.1:4566" if USE_LOCAL_AWS else None

# Example tool function
def list_s3_buckets():
    """List all S3 buckets."""
    s3 = boto3.client("s3", endpoint_url=ENDPOINT_URL)
    response = s3.list_buckets()
    return [bucket["Name"] for bucket in response.get("Buckets", [])]

# Map string names to actual Python functions
TOOL_REGISTRY = {
    "list_s3_buckets": list_s3_buckets
}

# Ollama-compatible tool schema definitions
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_s3_buckets",
            "description": "List all S3 buckets in the current AWS/LocalStack environment.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
]