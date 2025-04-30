def get_properties_from_graph(graph):
        """
        Wrapper for RDFLib.graph.predicates() that returns a unique set
        :param graph: RDFLib.graph
        :return: set, set of properties
        """
        # collapse to single list
        property_set = set()
        for row in graph.predicates():
            property_set.add(row)

        return property_set