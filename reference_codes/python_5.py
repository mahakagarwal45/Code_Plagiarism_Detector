def normalize_commit_message(commit_message):
    """
    Return a tuple of title and body from the commit message
    """
    split_commit_message = commit_message.split("\n")
    title = split_commit_message[0]
    body = "\n".join(split_commit_message[1:])
    return title, body.lstrip("\n")