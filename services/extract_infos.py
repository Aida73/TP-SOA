from xml.sax.saxutils import escape
from spyne.util.wsgi_wrapper import run_twisted
from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11
from spyne import Application, rpc, ServiceBase, Unicode, Integer, Iterable
import sys
import openai
import os
import re
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY


def getLoanInformations(letter):
    system_msg = 'You are a helpful assistant.'

    user_msg = f"""I want to extract information about the tenant from this letter, 
    such as his name, customer ID, description of what he wants to buy, address, 
    monthly income and expenses, price of the property he wants to buy, etc. 
    Here's the text: {letter}. You'll need to extract the result into a json. For the keys,you must 
    use camelcase. For the description, for example, create a json with the type 
    of accommodation, such as home or apartment, the surface area, such as 300m2, and the address 
    of the accommodation, such as town,code postal, all the interesting information
    about the accommodation.
    You also must not return text with the result.
    You just have to return the json that content elements. 
    Here is the schema you have to respect when returning results:
      {{{{"name": "John Doe",
        "customerId": "client_001",
        "description": {{
            "accommodationType": "apartment",
            "surfaceArea": "300m2",
            "address": {{
            "town": "Paris",
            "postalCode": "75015"
            }}
        }},
        "contact": {{
            "phone": "+33 5 67784890",
            "email": "johndoe@gmail.com"
        }},
        "loanAmount": 12000,
        "monthlyIncome": 3700,
        "monthlyExpenses": 2400,
        "propertyPrice": 20000
        }}}}"""

    # Create a dataset using GPT
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                                      {"role": "user", "content": user_msg}])
    status_code = response["choices"][0]["finish_reason"]
    assert status_code == "stop", f"The status code was {status_code}."
    return response["choices"][0]["message"]["content"]


class extractInformationsService(ServiceBase):
    @rpc(Unicode, _returns=Iterable(Unicode))
    def extraire_information(ctx, demande):
        infos = escape(getLoanInformations(demande))
        yield f'''{infos}'''


application = Application([extractInformationsService],
                          tns='spyne.examples.hello',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11()
                          )


if __name__ == '__main__':

    wsgi_app = WsgiApplication(application)

    twisted_apps = [
        (wsgi_app, b'extractInformationsService'),
    ]

    sys.exit(run_twisted(twisted_apps, 8002))
