import os

MLA_API_BASE_URL = os.getenv("MLA_API_BASE_URL", "https://api.mlalpha.com")
MLA_API_VERSION = os.getenv("MLA_API_VERSION", "v0.1")

MLA_API_URL = f"{MLA_API_BASE_URL}/{MLA_API_VERSION}"
