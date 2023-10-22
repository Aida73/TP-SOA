import requests
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
    response = requests.post(url, data=extract_enveloppeSOAP, headers=headers)
    return response.text

if __name__ == '__main__':
    extract_data_result = aproval(service_extract_inf_url,extract_enveloppeSOAP)
    print(extract_data_result)
