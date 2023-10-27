import openai
import os
import textract
from dotenv import load_dotenv
# OPENAI_API_KEY = "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"
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY


def extract_text(file_path):
    try:
        text = textract.process(file_path).decode("utf-8")
        return text
    except Exception as e:
        print(f"Error: {e}")
        return None


def getLoanInformations(letter):
    system_msg = 'You are a helpful assistant.'

    user_msg = f"I want to extract informations from this letter about the tenant like his name, his client id, the description de ce qu'il veut acheter,his address, his revenu mensuel et dépenses mensuelles, le prix du bien qu'il veut acheter, etc. Here is the text: {letter}. You will have to extract the result in a json with keys: Tenant informations.For the json values use camelcase for the keys. For the description for example, crete a json with the type of logement like home or appartement, the superficie like 300m2 et l'adresse du logement, like ville, code postale, all interesting informations about the logement"

    # Create a dataset using GPT
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                                      {"role": "user", "content": user_msg}])
    status_code = response["choices"][0]["finish_reason"]
    assert status_code == "stop", f"The status code was {status_code}."
    return response["choices"][0]["message"]["content"]


# print(getApiResponse(letter_text))
# Replace 'your_file.pdf' or 'your_file.docx' with the path to your file

print(getLoanInformations(extract_text('39057239-2.docx')))
