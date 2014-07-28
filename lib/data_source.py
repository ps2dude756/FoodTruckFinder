class DataSource:
    def __init__(self, item_data, header_data):
        self.item_data = item_data
        self.header_data = header_data

    def get_headers(self, headers, *args):
        """Obtain the indices of desired headers

        If the data is stored as lists rather than dictionaries, with a 
        separate list storing information about the headers, this function
        can be used to determine which indices contain the desired headers.
        
        Arguments:
        headers -- a set containing the names of headers to find the indices of
        *args -- any additional parameters needed to reach the header name.
                 For example, if your header info is stored as 
                 [{'meta': {'name': HEADER_NAME}}, ...], then *args should 
                 be set to ['meta', 'name'].
        """
        if not headers:
            return {}

        header_indices = {}
        for index, header_info in enumerate(self.header_data):
            for arg in args:
                header_info = header_info[arg]
           
            if header_info in headers:
                header_indices[header_info] = index

        return header_indices

    def gen_items(self, header_indices, *args):
        """Generator which yields selected info from an item

        Arguments:
        header_indices -- a dictionary mapping the name of a header, to the 
                          index of that component of an item. If the data is
                          stored as dictionaries, header_indices can be set to
                          {HEADER: HEADER}
        *args -- any additional parameters needed to reach an item.
                 For example, if your data is stored as 
                 [{'info': {'data': ITEM}}, ...], then *args should be set to
                 ['info', 'data']
        """
        if not header_indices:
            raise StopIteration

        for item in self.item_data:
            for arg in args:
                item = item[arg]

            row = {header: item[index] for header, index in header_indices.items()}
            yield row
