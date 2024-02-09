
def get_cli_from_chan_catalog(catalog, page=1):
    """
    Get a CLI representation of a chan catalog.
    :param catalog: The catalog to get the CLI representation of.
    """
    cli_output = f"Page {page}: \n"
    page = catalog[page-1]
    for thread in page.get("threads", []):
        subject = thread.get("sub", thread.get("com", "No subject")[0:64] + "...")
        replies = thread.get("replies", 0)
        cli_output += f" - {subject} ({replies} replies)\n"
    return cli_output
