from utils import createDatabases
from spyne.util.wsgi_wrapper import run_twisted
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
import sys
import logging
logging.basicConfig(level=logging.DEBUG)


def client_solvabilite(client_id):
    solvabilite = {}
    client_credit_data = createDatabases.CreditBureauDatabase.get_client_credit_data(
        client_id)
    if (client_credit_data == (0, 0, False)):
        solvabilite['clean'] = True
    else:
        solvabilite['clean'] = False
    revenu_mensuel, depense_mensuel = createDatabases.clientFinancialDatabase.get_client_financial_data(
        client_id)
    if depense_mensuel > revenu_mensuel:
        solvabilite['finacial_cap'] = True
    else:
        solvabilite['finacial_cap'] = False
    return solvabilite


class solvabiliteService(ServiceBase):
    @rpc(Unicode, _returns=Iterable(Unicode))
    def etudier_solvabilite(ctx, clientId):
        solvabilite = client_solvabilite(clientId)
        yield f"{solvabilite}"


application = Application([solvabiliteService],
                          tns='spyne.examples.hello',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )


if __name__ == '__main__':

    wsgi_app = WsgiApplication(application)

    twisted_apps = [
        (wsgi_app, b'solvabiliteService'),
    ]

    sys.exit(run_twisted(twisted_apps, 8003))
