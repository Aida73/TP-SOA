# TP-SOA

L'idée c'est de mettre en place un Service Web Composite qui permet l'évaluation de Demande de Prêt Immobilier. Il est conçu pour automatiser le processus d'évaluation
des demandes de prêt immobilier en utilisant des services Web spécialisés. Il permet aux clients de soumettre des demandes de prêt 
immobilier exprimées en langage naturel. Le service intègre des composants d’extraction des informations métiers de texte de la demande, 
de vérification de solvabilité, d'évaluation de la propriété et de décision d'approbation pour fournir une évaluation complète 
et précise des demandes de prêt.

# Demo

![Page_Web](/screenshots/demo-tp-soa.gif?raw=true)

## Variables d'environnement

Pour lancer le projet, vous devez:

Créer un fichier .env à la racine du projet et ajouter la clé openai qui permet d'utiliser l'Api openai:

`OPENAI_API_KEY=mykey`

Créer et activer un environnement virtuel. Vous pourrez utiliser des outils comme virtualenv ou conda.



## Installation

Installer les dépendances en se positionnant à la racine du projet:

```bash
  pip install -r requirements.txt
```
    
## Lancer le projet

Clone the project

```bash
    git clone [https://github.com/Aida73/ML-Tools-Project.git](https://github.com/Aida73/TP-SOA.git)
```

Se positionner à la racine du projet

```bash
    cd TP-SOA
```
Installer les dépendances en se positionnant à la racine du projet:

```bash
  pip install -r requirements.txt app.py
```
Lancer tous les services:

- Service extraction des informations du client:
  
```bash
    python services/extract-infos.py
```

- Service solvabilite:
  
```bash
    python services/solvabilte.py
```

- Service evaluation propriete:
  
```bash
    python services/eval-propriete.py
```

- Service composite(l'orchestrateur de tous les services):
  
```bash
    python services/composite.py
```

Pour que le pipeline commence à s'exécuter, il faut, après avoir activer tous les services ajouter une nouvelle lettre dans le dossier `depots`


