from .metabase import MetabaseClient, TchapClient, MetabaseMultipleProductsClient
from .datagouv import DataGouvClient, MessagerieClient, FranceTransfertClient
from .posthog import PostHogClient, VisioClient


all_adaptors = [
    MetabaseClient,
    MetabaseMultipleProductsClient,
    DataGouvClient,
    MessagerieClient,
    FranceTransfertClient,
    TchapClient,
    VisioClient,
    PostHogClient,
]
