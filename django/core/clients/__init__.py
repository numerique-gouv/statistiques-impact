from .datagouv import DataGouvClient, FranceTransfertClient, MessagerieClient
from .metabase import MetabaseClient, MetabaseMultipleProductsClient, TchapClient
from .posthog import PostHogClient

all_adaptors = [
    MetabaseClient,
    MetabaseMultipleProductsClient,
    DataGouvClient,
    MessagerieClient,
    FranceTransfertClient,
    TchapClient,
    PostHogClient,
]
