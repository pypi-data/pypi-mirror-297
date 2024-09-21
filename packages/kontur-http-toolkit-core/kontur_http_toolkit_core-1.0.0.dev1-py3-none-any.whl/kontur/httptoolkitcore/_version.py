from os import environ

ref_type = environ.get("GITHUB_REF_TYPE", False)
if ref_type == "tag":
    __version__ = environ.get("GITHUB_REF_NAME") or "0.dev0"
