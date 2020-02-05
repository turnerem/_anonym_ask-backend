a_session = {
    'session_name': 'Painting cars',
    'questions': [
      {
        'question': 'Are cars red?',
        'answers': {'Yes': 0, 'No': 0},
        'type': 'simple'
      },
      {
        'question': 'Should we use potato stencils on bonnet?',
        'answers': {'yes': 0, 'no': 0},
        'type': 'simple'
      },
      {
        'question': 'What sort of glitter should we use?',
        'answers': {'eco-friendly': 0, 'purple-green': 0, 'aquamarine with stars': 0},
        'type': 'multi'
      },
      {
        'question': 'What colour is your car passeger seat?',
        'answers': [],
        'type': 'text'
      }
    ]
  }

a_session_patch = {
    'session_name': 'Painting cars',
    'questions': [
      {
        'question': 'Are cars red?',
        'answers': {'Yes': 6, 'No': 1},
        'type': 'simple'
      },
      {
        'question': 'Should we use potato stencils on bonnet?',
        'answers': {'yes': 14, 'no': 12},
        'type': 'simple'
      },
      {
        'question': 'What sort of glitter should we use?',
        'answers': {'eco-friendly': 5, 'purple-green': 4, 'aquamarine with stars': 9},
        'type': 'multi'
      },
      {
        'question': 'What colour is your car passeger seat?',
        'answers': ['grey', 'grey', 'leather'],
        'type': 'text'
      }
    ]
  }