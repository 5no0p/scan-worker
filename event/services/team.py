def check_member_permissions(event_id, member_id, permission_id):
    """
    Check if the member has the specified permission
    :param event_id: Event id
    :param member_id: Member id
    :param permission_id: Permission id
    :return: True if the member has the specified permission
    """

    from users.selector import get_user_by_id
    
    # if event_id or member_id or permission_id is None:
    #     raise ValueError(f"event_id, member_id and permission_id cant be None. event_id={event_id} member_id={member_id} permission_id={permission_id}")

    return get_user_by_id(member_id).events_teams.filter(event_team__event=event_id).first().event_team.permissions.filter(permission__id=permission_id)

