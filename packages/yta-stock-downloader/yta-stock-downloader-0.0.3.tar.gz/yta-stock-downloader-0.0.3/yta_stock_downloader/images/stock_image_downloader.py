from yta_stock_downloader.images.stock_pexels_downloader import StockPexelsDownloader


class StockImageDownloader():
    """
    This object is useful to get and download stock images.
    """
    __instance = None

    def __new__(cls, ignore_repeated = True):
        if not StockImageDownloader.__instance:
            StockImageDownloader.__instance = object.__new__(cls)
        
        return StockImageDownloader.__instance

    def __init__(self, ignore_repeated = True):
        if not hasattr(self, 'ignore_repeated'):
            self.ignore_repeated = ignore_repeated
            self.pexels = StockPexelsDownloader(ignore_repeated)
            #self.pixabay = StockPixabayDownloader(ignore_repeated)