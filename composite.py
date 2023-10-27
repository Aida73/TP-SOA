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


def aproval(url, demande):
    headers = {'content-type': 'application/soap+xml; charset=utf-8'}
    response = requests.post(url, data=demande, headers=headers)
    return response.text


if __name__ == '__main__':
    print("-----------------------------------load texte--------------------------------------")
    letter_text = extract_text('39057239-2.docx')
    service_extract_inf_url = "http://0.0.0.0:8002/extractInformationsService"
    service_solvabilte_url = "http://0.0.0.0:8003/solvabiliteService"
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
    namespaces = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
                  'tns': 'spyne.examples.hello'}
    root = ET.fromstring(extract_data_result)
    response_element = root.find('.//tns:string', namespaces)
    response_text = response_element.text
    print("-----------------------------------extraction done--------------------------------------")
    client_infos = json.loads(response_text)
    # check solvabilite
    solvabilite_enveloppeSOAP = f'''\
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="spyne.examples.hello">
        <soapenv:Header/>
            <soapenv:Body>
                <spy:extraire_information>
                    <!--Optional:-->
                    <spy:clientId>{client_infos['tenantInformations']['clientId']}</spy:clientID>
                </spy:extraire_information>
            </soapenv:Body>
    </soapenv:Envelope>'''
    print("-----------------------------------check solvabilite begins--------------------------------------")
    solvabilite_data_result = aproval(
        service_solvabilte_url, solvabilite_enveloppeSOAP)
    print(solvabilite_data_result)
