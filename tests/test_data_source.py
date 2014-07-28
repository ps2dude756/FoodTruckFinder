import sys
import unittest

sys.path.insert(0, '../')

from lib.data_source import DataSource

ITEM_DATA = [
    [
        1, 
        '59D12C01-862C-4FD8-B6E1-53B21A1C03DE', 
        1, 
        1406388129, 
        '403253'
    ],
    [
        2, 
        '87437A5B-5C7B-444A-BBD5-1803D1B63422', 
        2, 
        1406388129, 
        '403253'
    ], 
    [
        3, 
        '76CBA7D9-8D51-47FE-B7C6-81437BC4B3A1', 
        3, 
        1406388129, 
        '403253'
    ], 
    [
        4, 
        '40A9F4FA-BC7E-49F0-9343-7E3EE160FFC7', 
        4, 
        1406388129, 
        '403253'
    ], 
    [
        5, 
        'D5FF0207-8D91-47DE-AA69-1B7AFE762F8F', 
        5, 
        1406388129, 
        '403253'
    ]
]

HEADER_DATA = [
    {
        'id' : -1,
        'name' : 'sid',
        'dataTypeName' : 'meta_data',
        'fieldName' : ':sid',
        'position' : 0,
        'renderTypeName' : 'meta_data',
    }, {
        'id' : -1,
        'name' : 'id',
        'dataTypeName' : 'meta_data',
        'fieldName' : ':id',
        'position' : 0,
        'renderTypeName' : 'meta_data',
    }, {
        'id' : -1,
        'name' : 'position',
        'dataTypeName' : 'meta_data',
        'fieldName' : ':position',
        'position' : 0,
        'renderTypeName' : 'meta_data',
    }, {
        'id' : -1,
        'name' : 'created_at',
        'dataTypeName' : 'meta_data',
        'fieldName' : ':created_at',
        'position' : 0,
        'renderTypeName' : 'meta_data',
    }, {
        'id' : -1,
        'name' : 'created_meta',
        'dataTypeName' : 'meta_data',
        'fieldName' : ':created_meta',
        'position' : 0,
        'renderTypeName' : 'meta_data',
    }
]

class Test_Data_Source(unittest.TestCase):
    def setUp(self):
        self.empty_data_source = DataSource([], [])
        self.data_source = DataSource(ITEM_DATA, HEADER_DATA)

    def test_get_headers_no_data_no_headers(self):
        expected = {}
        actual = self.empty_data_source.get_headers(set([]))
        self.assertEquals(expected, actual)

    def test_get_headers_no_data(self):
        expected = {}
        actual = self.empty_data_source.get_headers(set(['test']))
        self.assertEquals(expected, actual)

    def test_get_headers(self):
        expected = {
            'id': 1,
            'position': 2,
        }
        headers = set(['id', 'position'])
        actual = self.data_source.get_headers(headers, 'name')
        self.assertEquals(expected, actual)

    def test_get_headers_no_headers(self):
        expected = {}
        actual = self.data_source.get_headers(set([]))
        self.assertEquals(expected, actual)

    def test_get_headers_bad_header(self):
        expected = {
            'id': 1
        }
        headers = set(['id', 'abcdefg'])
        actual = self.data_source.get_headers(headers, 'name')
        self.assertEquals(expected, actual)

    def test_gen_items_no_data_no_headers(self):
        expected = []
        actual = [x for x in self.empty_data_source.gen_items({})]
        self.assertEquals(expected, actual)

    def test_gen_items_no_data(self):
        headers = {'sid': 0}

        expected = []
        actual = [x for x in self.empty_data_source.gen_items(headers)]
        self.assertEquals(expected, actual)

    def test_gen_items_no_headers(self):
        expected = []
        actual = [x for x in self.data_source.gen_items({})]
        self.assertEquals(expected, actual)

    def test_gen_items(self):
        headers = {'sid': 0}

        expected = [
            {'sid': 1},
            {'sid': 2},
            {'sid': 3},
            {'sid': 4},
            {'sid': 5}
        ]
        actual = [x for x in self.data_source.gen_items(headers)]
        self.assertEquals(expected, actual)

if __name__ == '__main__':
    unittest.main()
