#!/usr/bin/env python3
from parameterized import parameterized
from utils import access_nested_map, get_json
import unittest
from unittest.mock import patch, Mock



class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(context.exception.args[0], path[-1])

class TestGetJson(unittest.TestCase):
    """Unit tests for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        with patch('utils.requests.get') as mock_get:
            # Mock the .json() method to return test_payload
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            # Assert get_json returns the expected payload
            self.assertEqual(result, test_payload)

            # Assert requests.get was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)
