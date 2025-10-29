from .proconnect import ProConnectAdaptor
from .messagerie import MessagerieAdaptor
from .france_transfert import FranceTransfertAdaptor
from .tchap import TchapAdaptor
from .visio import VisioAdaptor


all_adaptors = [
    ProConnectAdaptor,
    FranceTransfertAdaptor,
    MessagerieAdaptor,
    TchapAdaptor,
    VisioAdaptor,
]
