import spacy
import re

# Charger un modèle de langue français
nlp = spacy.load("fr_core_news_md")

# Votre lettre en tant que texte brut
letter_text = """
John Doe
123 Main St
93380 – Pierrefitte-Sur-Seine
+33 5 67 784 890 
johndoe@gmail.com
		BNP
		567 Master St
		75015 – Paris
		Le 26 oct. 23

Objet : 
Demande de prêt immobilier	

	Madame, Monsieur,
	Je souhaite acquérir un bien immobilier qui nécessite un prêt bancaire. Client de votre établissement depuis le 12 Décembre 2012, je me tourne vers vous afin d’obtenir une solution de financement à même de concrétiser mon projet.
	La somme pour l’achat du bien est de 20000€. Je dispose d’un apport de 8000€.
	Le montant du prêt doit donc s’élever à 12000€. J’aimerai préciser que mon salaire mensuel en ce moment est 3700 € et mes dépenses mensuelles s’élèvent à 2400 €.
	Pour une prise en charge effective de ma demande, je vous fournis plusieurs justificatifs en complément de la lettre : pièce d’identité, avis d’imposition, RIB, bulletins de salaire... 
	Je vous remercie par avance pour votre retour sur les possibilités de financement. Je me tiens également à votre disposition pour un rendez-vous, ainsi que pour fournir d’éventuels justificatifs supplémentaires
	Veuillez agréer, Madame, Monsieur, mes salutations distinguées.
		John Doe

"""

# Analyser le texte avec spaCy
doc = nlp(letter_text)

# Extraire les entités pertinentes
tenant_name = ""
tenant_address = ""
loan_amount = None
monthly_income = None
monthly_expenses = None

print("ent", doc.ents)
for ent in doc.ents:
    print(ent)
    # if ent.label_ == "PER" and not tenant_name:
    #     tenant_name = ent.text
    # elif ent.label_ == "LOC" and not tenant_address:
    #     tenant_address = ent.text

    # if "salaire" in ent.text:
    #     print("ok")
    #     match = re.search(r'(\d+\s*€)', ent.text)
    #     if match:
    #         try:
    #             monthly_income = float(match.group(1).replace(
    #                 '€', '').replace(' ', '').replace(',', '.'))
    #         except ValueError:
    #             pass
    # if "depense" in ent.text:
    #     match = re.search(r'(\d+\s*€)', ent.text)
    #     if match:
    #         try:
    #             monthly_expenses = float(match.group(1).replace(
    #                 '€', '').replace(' ', '').replace(',', '.'))
    #         except ValueError:
    #             pass

# # Afficher les informations extraites
# print("Tenant's Name:", tenant_name)
# print("Tenant's Address:", tenant_address)
# print("Loan Amount:", loan_amount)
# print("Monthly Income:", monthly_income)
# print("Monthly Expenses:", monthly_expenses)
