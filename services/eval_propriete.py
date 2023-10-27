from spyne.util.wsgi_wrapper import run_twisted
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
import sys
import logging
logging.basicConfig(level=logging.DEBUG)


def estimer_valeur_propriete(taille_logement, ville):
    # Dictionnaire de valeurs de référence pour différentes villes
    valeurs_reference = {
        "Versailles": 300,
        "Paris": 350,
        "Nantes": 250
    }

    # Calculer la valeur estimée en fonction de la taille du logement et de la ville
    # Valeur par défaut si la ville n'est pas répertoriée
    valeur_par_metre_carre = valeurs_reference.get(ville, 200)
    valeur_estimee = taille_logement * valeur_par_metre_carre

    return valeur_estimee


class evaluationProprieteService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def evaluer_propriete(ctx, ville, taille_logement):
        valeur = estimer_valeur_propriete(taille_logement, ville)
        yield f"{valeur}"


application = Application([evaluationProprieteService],
                          tns='spyne.examples.hello',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )


if __name__ == '__main__':

    wsgi_app = WsgiApplication(application)

    twisted_apps = [
        (wsgi_app, b'evaluationProprieteService'),
    ]

    sys.exit(run_twisted(twisted_apps, 8004))
