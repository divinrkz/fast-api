user_dict = {
    'name': 'DIvin',
    'id': 1
}

user_dict['status'] = 'ACTIVE'
user_dict.pop('name')
# user_dict.clear()
print(user_dict.get('name'))

# del user_dict
for x, y in user_dict.items():
    print(x, y)

dict2 = user_dict.copy()