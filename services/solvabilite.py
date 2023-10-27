from utils import createDatabases
from spyne.util.wsgi_wrapper import run_twisted
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
import sys
import logging
logging.basicConfig(level=logging.DEBUG)


def client_solvabilite(client_id):
    # solvabilite = {}
    score = 0
    client_credit_data = createDatabases.CreditBureauDatabase.get_client_credit_data(
        client_id)
    if (client_credit_data == (0, 0, False)):
        score = 100
        # solvabilite['clean'] = True
    elif (client_credit_data[1] >= 2 and client_credit_data[2] == True):
        score = 0
    elif (client_credit_data[1] < 2 and client_credit_data[0] < 1000):
        score = 80
    elif (client_credit_data[1] < 2 and client_credit_data[0] > 1000):
        score = 60
    # else:
    #     solvabilite['clean'] = False
    revenu_mensuel, depense_mensuel = createDatabases.clientFinancialDatabase.get_client_financial_data(
        client_id)
    financial_cap = revenu_mensuel-depense_mensuel
    # if depense_mensuel > revenu_mensuel:
    #     solvabilite['finacial_cap'] = False
    # else:
    #     solvabilite['finacial_cap'] = True
    # if solvabilite['finacial_cap'] == True and solvabilite['clean'] == True:
    #     solvabilite['solvable'] = True
    # else:
    #     solvabilite['solvable'] = False
    return {'financial_cap': financial_cap, 'score': score}


class solvabiliteService(ServiceBase):
    @rpc(Unicode, _returns=Iterable(Unicode))
    def etudier_solvabilite(ctx, clientId):
        solvabilite = client_solvabilite(clientId)
        yield f'''{solvabilite}'''


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
