from core.exeptions import ModelCouldNotBeCreated

from event.models import Organizer

# def get_all_organizers():
#     return Organizer.objects.all()

def create_organizer(*args, **kwargs):
    try:
        organizer = Organizer.objects.create(*args, **kwargs)
        return organizer
    except ModelCouldNotBeCreated:
        raise ModelCouldNotBeCreated('Could not create Organizer model')

def create_new_organizer(user_id, short, slug=None):
    from users.selectors import select_user_by_id
    organizer_user = select_user_by_id(user_id)
    if not slug:
        slug = short.strip().replace(' ', '-')
    new_organizer = create_organizer(organizer=organizer_user, short=short, slug=slug)
    return new_organizer