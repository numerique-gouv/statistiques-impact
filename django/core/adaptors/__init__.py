from .proconnect import ProConnectAdaptor, LaSuiteAdaptor
from .messagerie import MessagerieAdaptor
from .france_transfert import FranceTransfertAdaptor
from .tchap import TchapAdaptor
from .visio import VisioAdaptor


all_adaptors = [
    ProConnectAdaptor,
    LaSuiteAdaptor,
    FranceTransfertAdaptor,
    MessagerieAdaptor,
    TchapAdaptor,
    VisioAdaptor,
]
