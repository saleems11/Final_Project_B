class AnchorsInSameCluster(Exception):
    pass


class SilhouetteBellowThreshold(Exception):
    def __init__(self, message, silhouette_val):
        super().__init__(message)
        self.silhouette_val = silhouette_val
