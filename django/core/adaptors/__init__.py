from .proconnect import ProConnectAdaptor
from .messagerie import MessagerieAdaptor
from .france_transfert import FranceTransfertAdaptor
from .tchap import TchapAdaptor

all_adaptors = [
    ProConnectAdaptor,
    FranceTransfertAdaptor,
    MessagerieAdaptor,
    TchapAdaptor,
]
