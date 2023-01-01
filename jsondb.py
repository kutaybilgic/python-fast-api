import json
from uuid import UUID

# filename = 'productdb.json'


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


def read_json(db):
    with open(db, 'r') as f:
        return json.load(f)


# add new product to productDb.json file
def write_json(db, data):
    with open(db, 'r+') as f:
        temp = json.load(f)
        print(data.__dict__)
        temp.append(data.__dict__)
        f.seek(0)
        json.dump(temp, f, cls=UUIDEncoder)
        f.truncate()

    # with open(filename, 'w') as f:
    #     json.dump(data.__dict__, f, cls=UUIDEncoder)


# find according to productName in productDb.json file
def find_product(db, productName):
    productDb = read_json(db)
    for product in productDb:
        if product['name'] == productName:
            return product
    return None


#  find according to userName in userDb.json file
def find_user(userName):
    userDb = read_json('userDb.json')
    for user in userDb:
        if user['username'] == userName:
            return user
    return None
