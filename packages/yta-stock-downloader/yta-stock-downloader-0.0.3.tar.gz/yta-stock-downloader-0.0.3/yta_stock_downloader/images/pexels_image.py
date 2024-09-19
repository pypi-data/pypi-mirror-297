class PexelsImage:
    def __init__(self, data):
        # TODO: Could be some of those fields unavailable?
        self.id = data['id']
        self.width = data['width']
        self.height = data['height']
        self.url = data['url']
        self.photographer = {
            'name': data['photographer'],
            'url': data['photographer_url'],
            'id': data['photographer_id'],
        }
        self.average_color = data['avg_color']
        """
        These are the different formats available: 'original', 
        'large2x', 'large', 'medium', 'small', 'portrait',
        'landscape' and 'tiny'
        """
        self.src = data['src']
        self.liked = data['liked']
        self.alt = data['alt']
        # We also store the raw data
        self.__json = data

    def json(self):
        return {
            'id': self.id,
            'width': self.width,
            'height': self.height,
            'url': self.url,
            'photographer': self.photographer,
            'average_color': self.average_color,
            'src': self.src,
            'liked': self.liked, 
            'alt': self.alt,
            #'json': self.__json
        }

        # TODO: I do it manually to fit the same structure
        return self.__json