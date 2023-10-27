import ast
import xml.etree.ElementTree as ET
import openai
import os
import requests
import json
import textract
from spyne.util.wsgi_wrapper import run_twisted
import re


def clean_text(text):
    pattern = r'[^\x00-\x7F]+'  # Matches non-ASCII characters
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def extract_text(file_path):
    try:
        text = textract.process(file_path).decode("utf-8")
        return clean_text(text)
    except Exception as e:
        print(f"Error: {e}")
        return None


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


if __name__ == '__main__':
    print("-----------------------------------load texte--------------------------------------")
    letter_text = extract_text('39057239-2.docx')
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
    print("-----------------------------------extraction begins--------------------------------------")
    extract_data_result = aproval(
        service_extract_inf_url, extract_enveloppeSOAP)
    print(extract_data_result)
    if extract_data_result:
        print("-----------------------------------extraction done--------------------------------------")
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
            print("-----------------------------------check solvabilite begins--------------------------------------")
            solvabilite_data_result = aproval(
                service_solvabilte_url, solvabilite_enveloppeSOAP)
            solvabilite_result = ast.literal_eval(
                getResults(solvabilite_data_result))
            solvable = solvabilite_result['solvable']
            print(solvable)
        # check propriete
        if client_infos['description']:
            evalPropriete_enveloppeSOAP = f'''\
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="spyne.examples.hello">
                <soapenv:Header/>
                    <soapenv:Body>
                        <spy:evaluer_propriete>
                            <!--Optional:-->
                            <spy:ville>{client_infos['description']['address']['town']}</spy:ville>
                            <!--Optional:-->
                            <spy:taille_logement>{int(client_infos['description']['surfaceArea'].split('m')[0])}</spy:taille_logement>
                        </spy:evaluer_propriete>
                    </soapenv:Body>
            </soapenv:Envelope>'''
            print("-----------------------------------evaluation propriete begins--------------------------------------")
            evalPropriete_data_result = aproval(
                service_evalPropriete_url, evalPropriete_enveloppeSOAP)
            evalPropriete_result = getResults(evalPropriete_data_result)
            print(evalPropriete_result)

    else:
        print("Some problem occurs. You can check your Api Key.")
