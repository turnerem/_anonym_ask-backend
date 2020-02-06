import os
from app import app
# import unittest
import pytest
import json
from test_data import a_session, a_session_patch

@pytest.fixture
def client():
  app.testing = True
  client = app.test_client()
  yield client

# def test_delete_user(client):
#   """DELETE user"""
#   resp = client.delete('/api/Shelves')
#   assert '204' in resp.status

def test_create_user(client):
  """cleanup workaround"""
  client.delete('/api/Kite')
  """POST new user"""
  resp = client.post('/api', data=json.dumps({"user_name": "Kite"}))
  assert '201' in resp.status
  """POST user that already exists"""
  resp = client.post('/api', data=json.dumps({"user_name": "Kite"}))
  assert '409' in resp.status

def test_get_user(client):
  """GET Kite"""
  resp = client.get('/api/Kite')
  assert '200' in resp.status
  py_dict = json.loads(resp.data)
  keys = list(py_dict.keys())
  assert len(keys) == 2
  assert isinstance(py_dict['sessions'], list)
  assert isinstance(py_dict['user_name'], str)
  """Get non-existent user"""
  resp = client.get('/api/dkfigjt')
  assert '404' in resp.status

def test_delete_user(client):
  client.post('/api', data=json.dumps({"user_name": "Mary"}))
  """DELETE existing user"""
  resp = client.delete('/api/Mary')
  assert '204' in resp.status
  """DELETE non-existent user"""
  resp = client.delete('/api/dkfigjt')
  assert '404' in resp.status

def test_post_session(client):
  """POST new session"""
  resp = client.post('/api/Kite', data=json.dumps(a_session))
  assert '200' in resp.status
  resp = client.post('/api/Kite4949', data=json.dumps(a_session))
  assert '409' in resp.status
  bad_session = {'session_name': 'flutes', 'questions': ['yes', 'no']}
  resp = client.post('/api/Kite', data=json.dumps(bad_session))
  assert '400' in resp.status

def test_get_session(client):
  """GET session"""
  resp = client.get('/api/Kite/Painting cars')
  assert '200' in resp.status
  """GET non-existent session"""
  resp = client.get('/api/Kite/Octopus')
  assert '404' in resp.status
  """GET session from non-existent user"""
  resp = client.get('/api/Mary/Octopus')
  assert '404' in resp.status

def test_patch_session(client):
  """PATCH session"""
  resp = client.patch('/api/Kite/Painting cars', data=json.dumps(a_session_patch))
  assert '200' in resp.status
  resp = client.get('/api/Kite/Painting cars')
  session = json.loads(resp.data)
  ans_samp = session['questions'][0]['answers']
  assert ans_samp['Yes'] == 6 
  assert ans_samp['No'] == 1

def test_delete_session(client):
  """DELETE session"""
  resp = client.delete('/api/Kite/Painting cars')
  assert '204' in resp.status
  resp = client.delete('/api/Kite/Painting Mars')
  assert '404' in resp.status
  
# class AppTests( unittest.TestCase ):
  
#   # def setUp(self):
#   #   app.app.testing = True
#   #   self.app = app.app.test_client()

#   # def test_api_username_get(self):
#   #   result = self.app.get('/api/JessJelly')
#   #   data = json.loads(result.data)
#   #   """
#   #   Test that response data is type dict
#   #   """
#   #   self.assertIsInstance(data, dict)
#   #   """
#   #   Test that number of sessions is 2
#   #   """
#   #   self.assertTrue(len(data['sessions']) == 2)

#   def test_add_user(self):
#     result = self.app.post('/api')
#     data = json.loads(result.data)
#     """
#     Test that response data is type dict
#     """
#     self.assertIsInstance(data, dict)



# # spaces in session name? spaces elseqhere?
# if __name__ == '__main__':
#   unittest.main()




#   import os
# import app
# import unittest
# # import pytest
# import json
# import pprint


# # class AppTests( unittest.TestCase ):
  
# #   def setUp(self):
# #     app.app.testing = True
# #     self.app = app.app.test_client()

# #   def test_api_username_get(self):
# #     result = self.app.get('/api/JessJelly')
# #     data = json.loads(result.data)
# #     """
# #     Test that response data is type dict
# #     """
# #     self.assertIsInstance(data, dict)
# #     """
# #     Test that number of sessions is 2
# #     """
# #     self.assertTrue(len(data['sessions']) == 2)

# #   # def test_add_user(self):
# #   #   result = self.app.post('/api', data={'user_name': 'banana'}))
# #   #   data = json.loads(result.data)
# #   #   """
# #   #   Test that response data is type dict
# #   #   """
# #   #   self.assertIsInstance(data, dict)



# # # spaces in session name? spaces elseqhere?
# # if __name__ == '__main__':
# #   unittest.main()