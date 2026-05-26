from .metabase import MetabaseClient, TchapClient, MetabaseMultipleProductsClient
from .datagouv import DataGouvClient, MessagerieClient, FranceTransfertClient
from .posthog import PostHogClient


all_indicators = [
    MetabaseClient,
    MetabaseMultipleProductsClient,
    DataGouvClient,
    MessagerieClient,
    FranceTransfertClient,
    TchapClient,
    PostHogClient,
]
