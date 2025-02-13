from os import environ
from pymongo import MongoClient
from .results_schema import ResultsSchema
from logging import getLogger
class MongoTransport():

    """
    This is the layer that will insert serialized ResultsSchema into the database.
    """

    config = None
    mongodb_uri = "mongodb://user:password@mongodb:27017/database"
    mongo_client = None
    db_acc = None
    db_collection = None
    recent_id = None


    def __init__(self, **kwargs):
        # TODO: Should the option to do all this be in the config file or not?
        self.log = getLogger(__name__)

        if "from_config" in kwargs:
            self.config = kwargs.get("from_config")

        # URI Options
        if self.config and self.config.mongodb_uri:
            self.mongodb_uri = self.config.mongodb_uri
        if environ.get("mongodb_uri"):
            self.mongodb_uri = environ.get("mongodb_uri")
        if "mongodb_uri" in kwargs:
            self.mongodb_uri = kwargs.get("mongodb_uri")

        # DB Selection.
        if self.config and self.config.results_db:
            self.results_db = self.config.results_db
        if environ.get("results_db"):
            self.mongodb_uri = environ.get("results_db")
        if "results_db" in kwargs:
            self.results_db = kwargs.get("results_db")

        # Collection Selection.
        if self.config and self.config.db_collection:
            self.db_collection = self.config.db_collection
        if environ.get("db_collection"):
            self.db_collection = environ.get("db_collection")
        if "db_collection" in kwargs:
            self.db_collection = kwargs.get("db_collection")

        self.log.debug(f"collection: {self.db_collection}")
        self.log.debug(f"results_db: {self.results_db}")
        self.log.debug(f"mongodb_uri: {self.mongodb_uri}")

        try:
            self.mongo_client = MongoClient(self.mongodb_uri)
        except Exception as err:
            raise Exception(err)
        else:
            self.db_acc = self.mongo_client[self.results_db]

    def add_data(self, data: dict):

        """
        This will actually add the data to the database. You should use the raw dictionary returned from
        the TrashcanMon.start_test().
        """

        if not isinstance(data, dict):
            raise TypeError(f"data is type({ type(data) }), and should be type({type(dict())})")

        try:
            results_added = self.db_acc[self.db_collection].insert_one(ResultsSchema(**data).dict(by_alias=True))
        except Exception as err:
            self.log.critical(err)
            raise Exception(err)
        else:
            self.recent_id = results_added.inserted_id
            self.log.debug(f"Added {results_added.inserted_id} to database.")
            return True

