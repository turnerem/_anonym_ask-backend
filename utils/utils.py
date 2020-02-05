def user_exists(db, user_name):
  names = db.list_collection_names()
  return names.count(user_name) > 0

def validate_sesh_struc(session):
  sesh_keys = list(session.keys())
  chk_sesh_keys = all(elem in sesh_keys for elem in ['session_name', 'questions'])
  if not chk_sesh_keys:
    return False

  chk_sesh_name = isinstance(session['session_name'], str)
  chk_qs = isinstance(session['questions'], list)
  a_question = session['questions'][0]
  chk_q = isinstance(a_question, dict)
  if not (chk_sesh_name & chk_qs & chk_q):
    return False

  q_keys = list(a_question.keys())
  chk_q_keys = (all(elem in q_keys for elem in ['question', 'answers', 'type']))
  if not (chk_q_keys):
    return False
  
  ans_set = a_question['answers']
  chk_ans = isinstance(ans_set, dict)
  ans_val_list = ans_set.values()
  chk_ans_vals = all([isinstance(val, int) for val in ans_val_list])
  if not (chk_ans_vals & chk_ans_vals):
    return False

  return True