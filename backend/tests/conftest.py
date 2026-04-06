import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../function"))

os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
os.environ.setdefault("AWS_ACCESS_KEY_ID", "testing")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "testing")
os.environ.setdefault("TABLE_NAME", "visitor-count")