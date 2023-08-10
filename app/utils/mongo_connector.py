from pymongo import MongoClient


class MongoConnector:
    def __init__(self):
        try:
            # self.client = MongoClient()
            self.client = MongoClient('localhost', 27017)
            print("Mongo DB connection created")
        except Exception as e:
            print(e)
            raise Exception(str(e))
    # example:- client = MongoClient(‘localhost’, 27017)

    def generic_selection(self, database_name=None, table_name=None, query=None):
        """
        Use to get data from collection
        :param database_name: str
        :param table_name: str
        :param query: str
        :return:
        """
        try:
            db = self.client[database_name]

            # Created or Switched to collection names
            collection = db[table_name]
            if query:
                collection_obj = collection.find({}, query)
            else:
                collection_obj = collection.find()
            query_result = [row for row in collection_obj]
            return query_result
        except Exception as e:
            print("error occurred while generic_selection")
            print(str(e))
            raise e

    def generic_selection_one(self, database_name=None, table_name=None, query=None):
        """
        Use to get data from collection
        :param database_name: str
        :param table_name: str
        :param query: str
        :return:
        """
        try:
            db = self.client[database_name]

            # Created or Switched to collection names
            collection = db[table_name]
            if query:
                collection_obj = collection.find_one(query)
            else:
                collection_obj = collection.find()
            query_result = collection_obj
            return query_result
        except Exception as e:
            print("error occurred while generic_selection")
            print(str(e))
            raise e

    def generic_insert_one(self, database_name=None, table_name=None, data=None):
        """
        Used to insert single record into collection
        :param database_name: str
        :param table_name: str
        :param data: dict
        :return: None
        """
        try:
            db = self.client[database_name]
            # Created or Switched to collection names
            collection = db[table_name]
            if isinstance(data, dict):
                collection.insert_one(data)
                return None
        except Exception as e:
            print("error occurred while inserting data")
            print(str(e))
            raise e

    def generic_insert_many(self, database_name=None, table_name=None, data=None):
        """
        Use to insert multiple record in collection
        :param database_name: str
        :param table_name: str
        :param data: list
        :return: none
        """
        try:
            db = self.client[database_name]
            # Created or Switched to collection names
            collection = db[table_name]
            if isinstance(data, list):
                collection.insert_many(data)
            else:
                print("error")
            return None
        except Exception as e:
            print("error occurred while inserting data")
            print(str(e))
            raise e

    def generic_update(self, database_name=None, table_name=None, selection_criteria=None, update_data=None):
        """
        Use to insert multiple record in collection
        :param selection_criteria:
        :param update_data: str
        :param selection_data: str
        :param database_name: str
        :param table_name: str
        :return: none
        """
        try:
            db = self.client[database_name]
            # Created or Switched to collection names
            collection = db[table_name]
            if isinstance(selection_criteria, dict) and isinstance(update_data, dict):
                collection.update_one(
                    selection_criteria, {"$push": update_data}
                )
            else:
                print("error")
            return None
        except Exception as e:
            print("error occurred while inserting data")
            print(str(e))
            raise e
