from mongodb_orm.interfaces.mongodb_model import MongoDBModel


class GenericModel(MongoDBModel):
    def __init__(self, tenant: str, collection: str, source_uri: str = None, **kwargs):
        if source_uri:
            self.source_uri = source_uri
        self.collection_name = collection
        super().__init__(tenant, **kwargs)
