from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class Dealer_Part(Consumer):
    """Inteface to Dealer_Part resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("dealers/parts")
    def list(
        self,
        company_uid: Query = None,
        company_branch_uid: Query = None,
        part_search_str: Query = None,
    ):
        """This call will return list of dealer parts."""

    @http_get("dealers/parts/{uid}")
    def get(self, uid: str):
        """This call will get the dealer part for the specified uid."""

    @delete("dealers/parts/{uid}")
    def delete(self, uid: str):
        """This call will delete the dealer part for the specified uid."""

    @delete("dealers/parts/branches/{uid}")
    def delete_by_company_branch(self, uid: str):
        """This call will delete the dealer part for the specified uid."""

    @returns.json
    @json
    @post("dealers/parts")
    def insert(self, dealer_part: Body):
        """This call will create the dealer part with the specified parameters."""

    @json
    @post("dealers/parts/batch")
    def insert_batch(
        self,
        dealer_part_list: Body,
        insert_method: Query = "bulk_save_objects",
    ):
        """This call will create the list of dealer parts with the specified parameters."""

    @json
    @patch("dealers/parts/{uid}")
    def update(self, uid: str, dealer_part: Body):
        """This call will update the dealer part with the specified parameters."""

    @json
    @patch("dealers/parts/batch")
    def update_batch(self, dealer_part_list: Body):
        """This call will update the list of dealer parts with the specified parameters. If the part doesn't exist, it will add the part."""
