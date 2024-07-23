from pymongo import MongoClient, errors
from bson.objectid import ObjectId

# Підключення до MongoDB
client = MongoClient('mongodb://localhost:27017/')  # змініть на свій URI, якщо використовуєте MongoDB Atlas
db = client['cat_database']
collection = db['cats']

def create_cat(name, age, features):
    try:
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        result = collection.insert_one(cat)
        print(f"Inserted cat with id: {result.inserted_id}")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")

def read_all_cats():
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")

def read_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("Cat not found")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")

def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Updated age for cat {name}")
        else:
            print("Cat not found")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")

def add_feature_to_cat(name, feature):
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": feature}})
        if result.matched_count > 0:
            print(f"Added feature to cat {name}")
        else:
            print("Cat not found")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")

def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Deleted cat {name}")
        else:
            print("Cat not found")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")

def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"Deleted {result.deleted_count} cats")
    except errors.PyMongoError as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    # Приклад використання функцій
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    read_all_cats()
    read_cat_by_name("barsik")
    update_cat_age("barsik", 4)
    add_feature_to_cat("barsik", "любить гратися з м'ячиком")
    delete_cat_by_name("barsik")
    delete_all_cats()