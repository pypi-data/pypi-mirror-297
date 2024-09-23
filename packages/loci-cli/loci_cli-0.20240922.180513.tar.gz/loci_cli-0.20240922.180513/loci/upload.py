import typer
from typing import Optional, List
from pathlib import Path
import os
import requests

from loci import utils


def upload(
    zipfiles: List[Path] = typer.Argument(
        ..., help="One or more zip files containing source code to upload."
    ),
    project_dir: Optional[str] = typer.Option(default=os.getcwd()),
    dry_run: bool = typer.Option(
        False, help="Show detailed info about what files will be uploaded."
    ),
):
    """
    Upload a zip file full of source code to the Loci Notes server.
    """
    # First get project info.
    project_info = utils.get_project_info(project_dir)

    # Check and make sure each file passed is a zip file.
    for src_code_zipfile in zipfiles:
        if not src_code_zipfile.is_file():
            utils.print_fatal(f"File [bold]{src_code_zipfile}[/bold] does not exist.")
        if src_code_zipfile.suffix != ".zip":
            utils.print_fatal(
                f"File [bold]{src_code_zipfile}[/bold] is not a zip file."
            )

    for src_code_zipfile in zipfiles:
        if dry_run:
            utils.print_info(f"Uploading {src_code_zipfile}... (dry run)")
            continue

        utils.print_info(f"Uploading {src_code_zipfile}...")

        headers = {
            "Authorization": "Bearer "
            + project_info.client_id
            + ":"
            + project_info.secret_key
        }

        with open(src_code_zipfile, "rb") as src_code_zipfile_fd:
            r = requests.post(
                f"{project_info.server}/api/v1/projects/{project_info.project_id}/zipfile",
                headers=headers,
                files={"file": src_code_zipfile_fd},
            )
            if r.status_code != 202:
                utils.print_error(f"Failed to upload {src_code_zipfile}.")
                r_dict = r.json()
                if "detail" in r_dict:
                    utils.print_error(r_dict["detail"])
                else:
                    utils.print_error(
                        "Something went wrong with the upload, and details were not provided. This is likely a bug."
                    )
                    utils.print_error(r.text)
                continue

    utils.print_info(
        "Please wait for the server to process the files (roughly a minute per uploaded file)."
    )
