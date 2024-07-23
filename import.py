import pymongo
import json

# Підключення до MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://bendello123:0oFsuBKLa9KlY1di@bendello.hckgjqk.mongodb.net/?retryWrites=true&w=majority&appName=bendello")
db = client['quotes_db']

# Завантаження та імпорт даних у колекцію authors
with open('authors.json', 'r', encoding='utf-8') as f:
    authors_data = json.load(f)
    db.authors.insert_many([{"name": name, **details} for name, details in authors_data.items()])

# Завантаження та імпорт даних у колекцію quotes
with open('quotes.json', 'r', encoding='utf-8') as f:
    quotes_data = json.load(f)
    db.quotes.insert_many(quotes_data)

print("Дані успішно імпортовані до MongoDB Atlas")
