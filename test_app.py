import os
import app
import unittest
# import pytest
import json
import pprint


class AppTests( unittest.TestCase ):
  
  def setUp(self):
    app.app.testing = True
    self.app = app.app.test_client()

  def test_api_username_get(self):
    result = self.app.get('/api/JessJelly')
    data = json.loads(result.data)
    """
    Test that response data is type dict
    """
    self.assertIsInstance(data, dict)
    """
    Test that number of sessions is 2
    """
    self.assertTrue(len(data['sessions']) == 2)

  def test_(self):
    result = self.app.get('/api/JessJelly/Painting')
    data = json.loads(result.data)
    """
    Test that response data is type dict
    """
    self.assertIsInstance(data, dict)



# spaces in session name? spaces elseqhere?