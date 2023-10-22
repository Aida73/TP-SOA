import re
import spacy
import json
import logging
logging.basicConfig(level=logging.DEBUG)
import sys
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.util.wsgi_wrapper import run_twisted
from xml.sax.saxutils import escape


def nlp_extract(texte):
    # Charger le modèle spaCy
    nlp = spacy.load("fr_core_news_md")

    # Traitement du texte avec spaCy
    doc = nlp(texte)

    # Initialisation d'un dictionnaire pour stocker les informations extraites
    resultat = {
        "prenom": "",
        "nom": "",
        "montant": "",
        "logement": ""
    }

    # Parcourir les tokens du texte
    for token in doc:
        if token.ent_type_ == "PER":  # Entité de type personne
            if not resultat["prenom"]:
                resultat["prenom"] = token.text
            else:
                resultat["nom"] = token.text

    # Utilisation d'une expression régulière pour extraire le montant
    montant_pattern = r'\d{1,10}(?:[.,]\d{1,2})? euros'
    montant_match = re.search(montant_pattern, texte)
    if montant_match:
        resultat["montant"] = montant_match.group(0)

    # Recherche du type de logement
    logement_idx = texte.find("pour un logement")
    if logement_idx != -1:
        resultat["logement"] = texte[logement_idx + len("pour un logement"):].strip()

    # Convertir le dictionnaire en JSON
    resultat_json = json.dumps(resultat, ensure_ascii=False, indent=4)

    # Afficher le résultat au format JSON
    return resultat_json

class extractionInformationService(ServiceBase):
    @rpc(Unicode,_returns=Iterable(Unicode))
    def extraire_information(ctx, demande):
        infos = escape(nlp_extract(demande))
        yield f'''{infos}'''

application = Application([extractionInformationService],
                        tns='spyne.examples.hello',
                        in_protocol=Soap11(validator='lxml'),
                        out_protocol=Soap11()
                    )


if __name__ == '__main__':

    wsgi_app = WsgiApplication(application)


    twisted_apps = [
        (wsgi_app, b'extractionInformationService'),
    ]

    sys.exit(run_twisted(twisted_apps,8001))