import openai
import os
import textract
import json
import re
from dotenv import load_dotenv
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

    user_msg = f"""I want to extract information about the tenant from this letter, 
    such as his name, customer ID, description of what he wants to buy, address, 
    monthly income and expenses, price of the property he wants to buy, etc. 
    Here's the text: {letter}. You'll need to extract the result into a json. For the keys,you must 
    use camelcase. For the description, for example, create a json with the type 
    of accommodation, such as home or apartment, the surface area, such as 300m2, and the address 
    of the accommodation, such as town,code postal, all the interesting information
    about the accommodation.
    You just have to return the json"""

    # Create a dataset using GPT
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{"role": "system", "content": system_msg},
                                                      {"role": "user", "content": user_msg}])
    status_code = response["choices"][0]["finish_reason"]
    assert status_code == "stop", f"The status code was {status_code}."
    json_pattern = r'\{(?:[^{}]|(?R))*\}'
    # Use re.findall to find all JSON objects in the global text
    json_objects = re.findall(
        json_pattern, response["choices"][0]["message"]["content"], re.DOTALL)
    # Parse each JSON object
    print(json_objects)
    for json_str in json_objects:
        try:
            json_data = json.loads(json_str)
            print("Found JSON object:")
            return (json_data)
        except json.JSONDecodeError:
            print("Found invalid JSON object:", json_str)


# print(getApiResponse(letter_text))
# Replace 'your_file.pdf' or 'your_file.docx' with the path to your file

print(getLoanInformations(extract_text('39057239-2.docx')))
