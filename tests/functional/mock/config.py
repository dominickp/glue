import os

REQUEST_TIMEOUT = 5
# TODO: document this envvar
GLUE_IMPLEMENTATIONS_CSV = os.environ.get("GLUE_IMPLEMENTATIONS_CSV")
if not GLUE_IMPLEMENTATIONS_CSV:
    raise ValueError("GLUE_IMPLEMENTATIONS_CSV environment variable not set")

# Split the GLUE_IMPLEMENTATIONS_CSV into a list of hostnames
GLUE_IMPLEMENTATIONS = GLUE_IMPLEMENTATIONS_CSV.split(",")
