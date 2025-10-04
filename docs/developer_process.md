# Developer Process Automation

To keep the repository free from inline Python comments, the project ships with
an automated cleanup utility and an accompanying GitHub Actions workflow.

## Comment removal script

`scripts/remove_python_comments.py` iterates over all git-tracked `*.py` files
and rewrites them without `#` style comments. Shebangs and encoding annotations
are preserved automatically. Run it locally with::

    python scripts/remove_python_comments.py --dry-run

Use the `--dry-run` flag to preview which files would change before applying the
rewrite.

## Scheduled workflow

The `.github/workflows/remove-python-comments.yml` workflow executes on a weekly
schedule (and is also available via the "Run workflow" button). It:

1. Checks out the repository and sets up Python.
2. Runs the comment removal script.
3. Creates a pull request with the sanitized files using the
   `peter-evans/create-pull-request` action.

If no files need to be updated the workflow simply exits without creating a
pull request.
