from spyne.util.wsgi_wrapper import run_twisted
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
import sys
import logging
logging.basicConfig(level=logging.DEBUG)


def verif_litiges(adresse_logement):

    adresses_avec_litiges = [
        "123 avenue Charles, Pierrefitte-sur-Seine",
        "456 Rue Louis, Versailles",
        "789 avenue Baudelaire, Mantes-la-Jolie"
    ]
    if adresse_logement in adresses_avec_litiges:
        return True
    else:
        return False


def estimer_valeur_propriete(taille_logement, ville, adresse):
    estimation = {
        "valeur": "",
        "litiges": "",
    }
    # Dictionnaire de valeurs de référence pour différentes villes
    valeurs_reference = {
        "Versailles": 300,
        "Paris": 350,
        "Nantes": 250
    }

    # Calculer la valeur estimée en fonction de la taille du logement et de la ville
    # Valeur par défaut si la ville n'est pas répertoriée
    valeur_par_metre_carre = valeurs_reference.get(ville, 200)

    # Estimation de la valeur de la propriete en se basant sur les prix du marche
    estimation["valeur"] = taille_logement * valeur_par_metre_carre
    estimation["litiges"] = verif_litiges(adresse)

    # Voir si le logement a des litiges ou pas
    return estimation


class evaluationProprieteService(ServiceBase):
    @rpc(Unicode, Integer, Unicode, _returns=Iterable(Unicode))
    def evaluer_propriete(ctx, ville, taille_logement, adresse):
        valeur = estimer_valeur_propriete(ville, taille_logement, adresse)
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
