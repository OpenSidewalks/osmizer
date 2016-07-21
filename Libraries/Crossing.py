from Libraries import Feature


class Crossing(Feature.Feature):
    def convert(self):
        """
        Convert curb ramps GeoJSON data to DOM tree, features may be duplicated due to the structure of JSON

        :return: a DOM tree structure which is equivalent to the sidewalk json database
        """
        # TODO: Implement convert
        raise NotImplementedError()
