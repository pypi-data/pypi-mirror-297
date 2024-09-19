from yta_stock_downloader.images.pexels_image import PexelsImage


class PexelsImagePageResult:
    """
    A class that represents the results obtained by firing an API image
    request. This will include information such as 'query', 'locale',
    'page', 'per_page', 'total_results', 'next_page_api_url' and
    'photos'.
    """
    def __init__(self, query, locale, data):
        self.query = query
        self.locale = locale
        self.page = data['page']
        self.per_page = data['per_page']
        self.total_results = data['total_results']
        # We calculate the total pages
        self.total_pages = (int) (self.total_results / self.per_page)
        if self.total_results % self.per_page > 0:
            self.total_pages += 1
        self.next_page_api_url = data['next_page'],
        self.photos = []

        for photo in data['photos']:
            self.photos.append(PexelsImage(photo))

    def json(self):
        return {
            'query': self.query,
            'locale': self.locale,
            'page': self.page,
            'per_page': self.per_page,
            'total_results': self.total_results,
            'total_pages': self.total_pages,
            'next_page_api_url': self.next_page_api_url,
            'photos': self.photos
        }

        # TODO: This below is not working
        from json import dumps as json_dumps

        return json_dumps(self.__dict__) 