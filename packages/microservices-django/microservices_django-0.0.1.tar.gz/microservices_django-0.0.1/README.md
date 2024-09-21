Install the package

setup in settings.py:

PROTOCOL = "http://"
DOMAIN = {
    'profile'(this is define variable): 'localhost:8001(this is domain)',
}

PATH = {
    'profile-create(this isdefine variable)': 'profiles/profile-create(this is api/path)',
}



for create:
user_data = {
    "uuid": str(user.uuid),
    "name": user.name
}
profile_create = CallEndpoint(self.request, 'profile'(this is varable of Domain which is define in settings), 'profile-create'(this is varable of path)).create(user_data)


for read all data:
profile_list = CallEndpoint(self.request, 'profile', 'profile-list').get()


for get specific data by using id/uuid:
profile_detail = CallEndpoint(self.request, 'profile', 'profile-detail').get_detail(id or uuid)


for update:
profile_update = CallEndpoint(self.request, 'profile', 'profile-update').update(id or uuid, data)


for delete:
profile_delete = CallEndpoint(self.request, 'profile', 'profile-delete').delete(id or uuid)
