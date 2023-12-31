import ast
import xml.etree.ElementTree as ET
import openai
import os
import requests
import json
import textract
from spyne.util.wsgi_wrapper import run_twisted
import re
from file_listener import *


def getResults(data):
    namespaces = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
                  'tns': 'spyne.examples.hello'}
    root = ET.fromstring(data)
    response_element = root.find('.//tns:string', namespaces)
    return response_element.text


def aproval(url, demande):
    headers = {'content-type': 'application/soap+xml; charset=utf-8'}
    response = requests.post(url, data=demande, headers=headers)
    return response.text


def decision(valeur, propertyPrice, litiges, score, financial_cap):
    if (valeur <= propertyPrice) and (litiges == True) and (score > 50 and (financial_cap > 0)):
        return f"Bonjour Monsieur {client_infos['name']}, après étude de votre dossier, nous avons le plaisir de vous annoncer que le prêt pourra vous être accordé. Passer très vite à l'agence pour signer tous les documents nécessaires."
    return f"Bonjour Monsieur {client_infos['name']}, après étude de votre dossier, nous avons le regret de vous annoncer que votre situation actuelle ne vous permet pas de contracter ce prêt. Nous vous conseillons de revenir d'ici 6mois pour une nouvelle étude."


if __name__ == '__main__':
    print("-----------------------------------listen to new file-------------------------------------")
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_path)
    observer.start()
    try:
        while True:
            if event_handler.should_stop_processing():
                break
            newly_created_file = event_handler.get_newly_created_file()
            if newly_created_file:
                print(
                    "-----------------------------------load texte--------------------------------------")
                letter_text = extract_text(newly_created_file)
                service_extract_inf_url = "http://0.0.0.0:8002/extractInformationsService"
                service_solvabilte_url = "http://0.0.0.0:8003/solvabiliteService"
                service_evalPropriete_url = "http://0.0.0.0:8004/evaluationProprieteService"
                extract_enveloppeSOAP = f'''\
                    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="spyne.examples.hello">
                        <soapenv:Header/>
                            <soapenv:Body>
                                <spy:extraire_information>
                                    <!--Optional:-->
                                    <spy:demande>{letter_text}</spy:demande>
                                </spy:extraire_information>
                            </soapenv:Body>
                    </soapenv:Envelope>'''
                print(
                    "-----------------------------------extraction begins--------------------------------------")
                extract_data_result = aproval(
                    service_extract_inf_url, extract_enveloppeSOAP)
                if extract_data_result:
                    print(
                        "-----------------------------------extraction done--------------------------------------")
                    client_infos = json.loads(getResults(extract_data_result))
                    # check solvabilite
                    if client_infos['customerId']:
                        solvabilite_enveloppeSOAP = f'''\
                            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="spyne.examples.hello">
                                <soapenv:Header/>
                                    <soapenv:Body>
                                        <spy:etudier_solvabilite>
                                            <!--Optional:-->
                                            <spy:clientId>{client_infos['customerId']}</spy:clientId>
                                        </spy:etudier_solvabilite>
                                    </soapenv:Body>
                            </soapenv:Envelope>'''

                        print(
                            "-----------------------------------check solvabilite begins--------------------------------------")
                        solvabilite_data_result = aproval(
                            service_solvabilte_url, solvabilite_enveloppeSOAP)
                        solvabilite_result = ast.literal_eval(
                            getResults(solvabilite_data_result))
                    # check propriete
                    if client_infos['description']:
                        if 'completeAdress' in client_infos['description']['address'].keys():
                            evalPropriete_enveloppeSOAP = f'''\
                                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="spyne.examples.hello">
                                    <soapenv:Header/>
                                        <soapenv:Body>
                                            <spy:evaluer_propriete>
                                                <!--Optional:-->
                                                <spy:ville>{client_infos['description']['address']['town']}</spy:ville>
                                                <!--Optional:-->
                                                <spy:taille_logement>{int(client_infos['description']['surfaceArea'].split('m')[0])}</spy:taille_logement>
                                                <!--Optional:-->
                                                <spy:adresse>{client_infos['description']['address']['completeAdress']}</spy:adresse>
                                            </spy:evaluer_propriete>
                                        </soapenv:Body>
                                </soapenv:Envelope>'''
                        else:
                            evalPropriete_enveloppeSOAP = f'''\
                                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="spyne.examples.hello">
                                    <soapenv:Header/>
                                        <soapenv:Body>
                                            <spy:evaluer_propriete>
                                                <!--Optional:-->
                                                <spy:ville>{client_infos['description']['address']['town']}</spy:ville>
                                                <!--Optional:-->
                                                <spy:taille_logement>{int(client_infos['description']['surfaceArea'].split('m')[0])}</spy:taille_logement>
                                                <!--Optional:-->
                                                <spy:adresse>{client_infos['description']['address']['completeAddress']}</spy:adresse>
                                            </spy:evaluer_propriete>
                                        </soapenv:Body>
                                </soapenv:Envelope>'''
                        print(
                            "-----------------------------------evaluation propriete begins--------------------------------------")
                        evalPropriete_data_result = aproval(
                            service_evalPropriete_url, evalPropriete_enveloppeSOAP)
                        evalPropriete_result = ast.literal_eval(getResults(
                            evalPropriete_data_result))
                        # print(evalPropriete_result)
                    # ----------------------------------------Start approal-------------------------------------------------------#
                    print(decision(evalPropriete_result['valeur'], client_infos['propertyPrice'],
                          evalPropriete_result['litiges'], solvabilite_result['score'], solvabilite_result['financial_cap']))

                event_handler.set_stop_condition(True)
    except KeyboardInterrupt:
        pass
