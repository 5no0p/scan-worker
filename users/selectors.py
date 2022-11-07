from django.contrib.auth import get_user_model

"""
    All fetching data from the database.
"""

User = get_user_model()

def select_user_by_id(user_id):
    """
        Return the user data for the specified user_id.
    """
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        raise User.DoesNotExist(f"User with id {user_id} does not exist")