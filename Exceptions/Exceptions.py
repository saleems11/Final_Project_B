
class AnchorsInSameCluster(Exception):
    """ A class used to throw specific type of exceptions"""
    pass


class SilhouetteBellowThreshold(Exception):
    """ A class used to throw specific type of exceptions, and save the silhouette_val"""
    def __init__(self, message, silhouette_val):
        super().__init__(message)
        self.silhouette_val = silhouette_val
