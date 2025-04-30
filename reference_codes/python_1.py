def attrib(self):
        """
        General XML element attributes for a seismic source, as a dict.
        """
        return dict([
            ('id', str(self.id)),
            ('name', str(self.name)),
            ('tectonicRegion', str(self.trt)),
        ])