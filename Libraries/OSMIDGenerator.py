import uuid


class OSMIDGenerator:
    def __init__(self):
        super().__init__()

    def get_next(self):
        """
        Generate the next unique OSM object id

        :return: an integer representing the ID
        """
        # UUID Hashing Doc: https://docs.python.org/3/library/uuid.html#uuid.uuid4
        new_uuid = uuid.uuid4()
        return -int(new_uuid.time_low)
