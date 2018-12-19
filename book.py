from flask import Flask
from flask_restplus import Api, Resource, fields


app = Flask(__name__)
api = Api(app, version="1.0", title="Book API", description="an APi for test")


all_books = [
    {"name": "Assoud", "author": "Almaaari"},
    {"name": "Animal Farm", "author": "George Orwell"},
]

book_model = api.model(
    "book",
    {
        "name": fields.String("name of the book"),
        "author": fields.String("author of the book"),
    },
)


@api.route("/books")
class AllBooks(Resource):
    @api.marshal_with(book_model, envelope="data")
    def get(self):
        """
          get all the book

        """
        return all_book, 200

    @api.expect(book_model)
    def post(self):
        """
           add new book to the list
        """
        new_book = api.payload
        all_books.append(new_book)
        return {"result": "Book added"}, 201


@api.route("/author/<author>")
class Author(Resource):
    @api.marshal_with(book_model, envelope="data")
    def get(self, author):
        """
       get all the book by the aythor

       """

        result = [book for book in all_books if book["author"] == author]
        return result


parser = api.parser()
parser.add_argument(
    "author", type=str, required=True, help="name of the author", location="form"
)


@api.route("/book/<book>")
class Book(Resource):
    @api.marshal_with(book_model, envelope="data")
    def get(self, book_name):
        """
         get book whith name

      """
        result = [book for book in all_books if book["name"] == book_name]
        return result

    @api.doc(parser=parser)
    def put(self, book_name):
        """

        modify detail of the book

        """
        args = parser.parse_args()

        for index, book in enumerate(all_books):
            if book["name"] == book_name:
                all_books[index]["author"] = args["author"]
                return book, 201
        return None, 201

    def delete(self, book_name):
        """
        delete the book

        """
        for index, book in enumerate(all_books):
            if book["name"] == book_name:
                del all_books[index]
                return {"response": "book deleted"}, 204
        return None, 404


if __name__ == "__main__":
    app.run(debug=True)
