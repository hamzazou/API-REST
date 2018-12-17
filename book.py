from flask import Flask
from flask_restplus import Api, Resource, fields


app = Flask(__name__)
api = Api(app, version='1.0', title='Book API', description='an APi for test')


all_books = [
    {
        "name": "Assoud",
        "author": "Almaaari"
    },
    {
        "name": "Animal Farm",
        "author": "George Orwell"
    }
]

book_model = api.model("book", { "name": fields.String("name of the book"), "author": fields.String("author of the book")})

@api.route('/books')
class AllBooks(Resource):
     
    @api.marshal_with(book_model, envelope='data')
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
        return {'result': 'Book added'}, 201

@api.route('/author/<author>')
class Author(Resource):

    @api.marshal_with(book_model, envelope='data') 
    def get(self, author):
       """
       get all the book by the aythor

       """

       result = [book for book in all_books if book['author'] == author]
       return result

if __name__ == '__main__':
    app.run(debug=True)
