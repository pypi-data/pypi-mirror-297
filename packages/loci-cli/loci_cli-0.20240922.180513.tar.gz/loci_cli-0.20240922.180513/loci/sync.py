import shutil
import uuid
import zipfile
import loci_client.models
import typer
from typing import Optional
from pathlib import Path
import os
from rich.progress import Progress
import requests

import loci_client
from loci import utils


def sync(
    project_dir: Optional[str] = typer.Option(default=os.getcwd()),
    dry_run: bool = typer.Option(
        False, help="Show detailed info about what files will be downloaded."
    ),
):
    """
    Sync the local code folder with all code from the Loci Notes server.
    """
    # First get project info.
    project_info = utils.get_project_info(project_dir)

    src_code_dir = Path(project_dir) / "_src"
    src_code_dir.mkdir(parents=True, exist_ok=True)

    tmp_src_dir = Path(project_dir) / ".locitmp"
    tmp_src_dir.mkdir(parents=True, exist_ok=True)

    # Get a listing of all source code files in the project.
    utils.print_info("Grabbing a list of all source code files in the project...")
    api_client = utils.get_api_client(project_info)
    with api_client:
        api_instance = loci_client.DefaultApi(api_client)

        id = project_info.project_id
        type = loci_client.ArtifactTypeEnum.SOURCE_CODE_FILE
        sort = loci_client.ArtifactSortEnum.CREATED_AT
        order = loci_client.OrderByEnum.DESC
        skip = 0
        limit = 100

        try:
            api_response = api_instance.read_project_artifacts(
                id,
                skip=skip,
                limit=limit,
                type=type,
                sort=sort,
                order=order,
            )

            for artifact in api_response.data:
                # First we need to see if we already have the repos that this file refers to.
                # If we don't, we need to download them.
                known_repos = []

                for note_id in artifact.note_ids:
                    note = api_instance.read_note(note_id)
                    if (
                        note.type == loci_client.ArtifactNoteTypeEnum.METADATA_KV
                        and note.contents.startswith("ZIPFILE_REPO:")
                    ):
                        known_repos.append(note.contents[13:])

                all_repos_correct = True
                for repo in known_repos:
                    # Check if the folder exists. We assume that if the folder exists, then it is correct.
                    repo_dir = src_code_dir / Path(repo)
                    if not repo_dir.exists() and not repo_dir.is_dir():
                        all_repos_correct = False
                        break

                if all_repos_correct:
                    # We already have the files that we would get by downloading this artifact file.
                    continue

                # We need to download the artifact file and extract it first to the tmp src dir, then the real
                # one. This isn't quite atomic, but it's close enough.
                file_info = api_instance.get_artifact_file(artifact.id)

                if dry_run:
                    utils.print_info(f"Downloading {file_info.filename}... (dry run)")
                    continue

                utils.print_info(f"Downloading {file_info.filename}...")

                with Progress() as progress:
                    with requests.get(file_info.link) as r:
                        r.raise_for_status()

                        total = int(r.headers["Content-Length"])
                        task = progress.add_task("Downloading...", total=total)
                        with open(tmp_src_dir / artifact.descriptor, "wb") as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                                progress.update(task, advance=len(chunk))

                # Extract the file.
                utils.print_info(f"Extracting {artifact.descriptor}...")
                tmp_dir_uuid = str(uuid.uuid4())
                tmp_extract_dir = tmp_src_dir / tmp_dir_uuid
                tmp_extract_dir.mkdir(parents=True, exist_ok=True)
                with zipfile.ZipFile(tmp_src_dir / artifact.descriptor, "r") as archive:
                    archive.extractall(tmp_extract_dir)

                # Move the files to the correct location.
                for root, dirs, files in os.walk(tmp_extract_dir):
                    for dir in dirs:
                        src_dir = Path(root) / dir
                        shutil.move(src_dir, src_code_dir)

        except loci_client.ApiException as e:
            utils.handle_exception(e)

    utils.print_success("Sync complete.")
