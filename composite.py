import xml.etree.ElementTree as ET
import requests
import json

service_extract_inf_url = "http://0.0.0.0:8001/extractionInformationService"
extract_enveloppeSOAP = '''\
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spy="spyne.examples.hello">
    <soapenv:Header/>
        <soapenv:Body>
            <spy:extraire_information>
                <!--Optional:-->
                <spy:demande>Je m'appelle Michel Seck et je souhaite emprunter 200000 euros pour un logement de 300 m2 a Paris.</spy:demande>
            </spy:extraire_information>
        </soapenv:Body>
</soapenv:Envelope>'''

def aproval(url,demande):
    headers = {'content-type':'application/soap+xml; charset=utf-8'}
    response = requests.post(url, data=demande, headers=headers)
    return response.text



if __name__ == '__main__':
    extract_data_result = aproval(service_extract_inf_url,extract_enveloppeSOAP)
    namespaces = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/', 'tns': 'spyne.examples.hello'}
    root = ET.fromstring(extract_data_result)
    response_element = root.find('.//tns:string', namespaces)
    response_text = response_element.text
    client_infos = json.loads(response_text)
    print(client_infos['montant'])
    