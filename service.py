from api import IdealistaClient
from builder import SearchFilterBuilder


class IdealistaService(IdealistaClient):
    def __init__(self):
        super().__init__()

    def search_with_paginated_results(self, search_builder: SearchFilterBuilder):
        page = 1
        total_pages = None

        while True:
            search_builder = search_builder.set_num_page(page)
            response = self.search(search_builder.build())
            response_data = response.json()

            if total_pages is None:
                total_pages = response_data['totalPages']

            if response.status_code == 407:
                print("WARNING: API rate limit reached")
                continue

            yield from response_data['elementList']

            print(f"Fetching page {page}/{total_pages}")
            if page >= total_pages:
                break

            page += 1
