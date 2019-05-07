def get_desired_age_range(user_pref_age='b'):
    """
        Will convert a user's preferred age in to a range of ages which are needed
        to properly query dogs based on user preferences.

        :age: b, y, a, or s
    """
    if user_pref_age not in ['b', 'y', 'a', 's']:
        raise ValueError('An accepted age was not provided.')
    acceptable_ages = {
      'b': range(0, 13), # 0 - 12 mo
      'y': range(13, 37), # 13 - 36 mo
      'a': range(37, 85), # 37 - 84 mo
      's': range(85, 241) # 85 - 240 mo 
    }
    desired_age_range = [i for i in acceptable_ages[user_pref_age]]
    return desired_age_range