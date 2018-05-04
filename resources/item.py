from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank (custom typed message!)"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
    )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() #returns the item object
        return {'message': 'Item not found'}, 404

    def post(self, name): #CRUD - create (post), read (get), update (put), delete (del)
        if ItemModel.find_by_name(name ): #checking that the item does not exist in the db
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args() #parse the data with parser

#        item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data) #same as above

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500 #internal server error

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name): #PUT can update or create existing item, call 10 PUT requests of same item and you will have just one item updated 10 times
        data = Item.parser.parse_args() #calls from the top level parser function

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]} #both work, more pythonic
#        return {'items': lists(map(lambda x: x.json(), ItemModel.query.all()))} #both work, only use if you're also using another langaugee
