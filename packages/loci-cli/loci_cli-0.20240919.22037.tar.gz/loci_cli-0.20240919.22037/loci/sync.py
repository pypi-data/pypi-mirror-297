import loci_client.models
import typer
from typing import Optional
from pathlib import Path
import os
from rich.progress import Progress
import concurrent.futures
import requests

import loci_client
from loci import utils


def _sync_single_file(
    artifact: loci_client.models.ArtifactOut,
    src_code_dir: str,
    dry_run: bool,
    project_info: utils.ProjectConfig,
) -> None:

    # This is the ultimate location of the source code file.
    src_code_filename = artifact.descriptor
    src_code_file_fq = src_code_dir / src_code_filename

    # See if the file already exists. If it does, compare the hashes to see if it's the right version.
    if src_code_file_fq.exists() and not src_code_file_fq.is_dir():
        # TODO at some point we should check versions, but for now we'll just keep going.
        return

    if dry_run:
        utils.print_info(
            f"The file [bold]{src_code_filename}[/bold] will be downloaded (dry run)"
        )
        return

    # So it turns out that the API client doesn't do well with handling downloadable files. So we're
    # going to do it manually.
    server = project_info.server
    client_id = project_info.client_id
    client_secret = project_info.secret_key

    full_url_path = f"{server}/api/v1/artifacts/{artifact.id}/file"
    headers = {
        "Authorization": "Bearer " + client_id + ":" + client_secret,
        "Accept": "application/octet-stream,plain/text",
    }
    r = requests.get(full_url_path, headers=headers)
    if r.status_code != 200:
        utils.print_error(
            f"Failed to download {artifact.descriptor} [ID {artifact.id}]."
        )
        return

    os.makedirs(os.path.dirname(src_code_file_fq), exist_ok=True)
    with open(src_code_file_fq, "wb") as f:
        f.write(r.content)


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
        limit = 1

        try:
            # For this first call, we just need the count.
            api_response = api_instance.read_project_artifacts(
                id,
                skip=skip,
                limit=limit,
                type=type,
                sort=sort,
                order=order,
            )

            total_count = api_response.count

        except loci_client.ApiException as e:
            utils.handle_exception(e)

        total_processed = 0

        with Progress() as progress:
            # for i in track(range(total_count), description="Syncing files to host..."):

            task = progress.add_task("Syncing files...", total=total_count)

            while total_processed < total_count:

                skip = total_processed
                limit = 100

                current_artifacts = []

                try:
                    # Read Project Artifacts
                    api_response = api_instance.read_project_artifacts(
                        id,
                        skip=skip,
                        limit=limit,
                        type=type,
                        sort=sort,
                        order=order,
                    )

                    for artifact in api_response.data:
                        current_artifacts.append(artifact)

                except loci_client.ApiException as e:
                    utils.handle_exception(e)

                # "But you should have a dynamic thread pool size!" I hear you say. Yes, I should. But I don't want to
                # deal with multiple people pulling down 1000s of files at once, and maxing out the server
                # DB connection pool again. So I'm setting a hard limit of 16 threads.
                thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=16)

                futures_list = []

                for artifact in current_artifacts:
                    future = thread_pool.submit(
                        _sync_single_file,
                        artifact=artifact,
                        src_code_dir=src_code_dir,
                        dry_run=dry_run,
                        project_info=project_info,
                    )
                    futures_list.append(future)

                for future in futures_list:
                    # This is actually terrible, but better than nothing. Technically we are waiting for the OLDEST
                    # future in each iteration, not the first one that completes.
                    future.result()
                    total_processed += 1
                    progress.update(task, advance=1)

                thread_pool.shutdown(wait=True)

    utils.print_success("Sync complete.")
    utils.print_info(f"Synced {total_processed} files.")
