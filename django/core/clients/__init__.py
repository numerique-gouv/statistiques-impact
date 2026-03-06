from .metabase import MetabaseClient, TchapClient, MetabaseMultipleProductsClient
from .datagouv import FranceTransfertAdaptor, MessagerieAdaptor
from .posthog import PostHogClient, VisioClient


all_adaptors = [
    MetabaseClient,
    MetabaseMultipleProductsClient,
    FranceTransfertAdaptor,
    MessagerieAdaptor,
    TchapClient,
    VisioClient,
    PostHogClient,
]
