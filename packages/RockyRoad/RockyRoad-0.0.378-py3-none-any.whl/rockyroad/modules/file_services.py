from pickle import FALSE
from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class File_Services(Consumer):
    """Inteface to Inspection resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @multipart
    @post("services/files/upload-files/{container_name}")
    def uploadFile(
        self,
        container_name: str,
        file: Part,
        directory: Query,
        overwrite: Query = False,
        storage_account: Query = None,
    ):
        """This call will upload a file."""

    @returns.json
    @http_get("services/files/list-files/{container_name}")
    def listFiles(
        self,
        container_name: str,
        directory: Query,
        recursive: Query = True,
        storage_account: Query = None,
    ):
        """This call will return a list of the files by args."""

    @http_get("services/files/download-files/{container_name}/{file_name}")
    def downloadFile(
        self,
        container_name: str,
        file_name: str,
        directory: Query,
        storage_account: Query = None,
    ):
        """This call will download the file associated with the params."""

    @delete("services/files/delete-directory/{container_name}")
    def deleteDirectory(
        self,
        container_name: str,
        directory: Query,
        storage_account: Query = None,
    ):
        """This call will delete a directory and all the files in it."""

    @delete("services/files/delete-file/{container_name}/{file_name}")
    def deleteFile(
        self,
        container_name: str,
        file_name: str,
        directory: Query,
        storage_account: Query = None,
    ):
        """This call will delete a file"""

    @delete(
        "services/files/datalake-accounts/{storage_account}/containers/{container_name}"
    )
    def deleteDatalakeDirectory(
        self,
        container_name: str,
        directory: Query,
        storage_account: str,

    ):
        """This call will delete a directory from an Azure datalake."""
