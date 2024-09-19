from yta_stock_downloader.images.stock_image_downloader import StockImageDownloader

class StockDownloader:
    """
    An object to interact with Stock media platforms. This object integrates different
    APIs to work with those platforms.

    This object is useful to get and download stock videos and images.
    """
    __instance = None

    def __new__(cls, ignore_repeated = True):
        if not StockDownloader.__instance:
            StockDownloader.__instance = object.__new__(cls)
        
        return StockDownloader.__instance

    def __init__(self, ignore_repeated = True):
        if not hasattr(self, 'ignore_repeated'):
            self.ignore_repeated = ignore_repeated
            self.image = StockImageDownloader(ignore_repeated)
            # TODO: Implement video downloader
            #self.video = StockVideoDownloader(ignore_repeated)
