from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# Chargez le fichier CSV dans un dictionnaire
def lire_base_donnees():
    base_donnees= []
    with open('basse_donnees.csv', newline='', encoding='utf-8') as csvfile:
        lecteur_csv = csv.DictReader(csvfile)
        for ligne in lecteur_csv:
            base_donnees.append(ligne)
    return base_donnees

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        numero = request.form['numero']
        
        # Chercher l'utilisateur dans la base de données uniquement par numéro de téléphone
        base_donnees = lire_base_donnees()
        utilisateur = next((u for u in base_donnees if u['Numéro téléphone'] == numero), None)
        
        if utilisateur:
            # ID utilisateur trouvé, on affiche le lien du formulaire Google
            google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfac4EIrtXxHmgQfGbe2RiHb0JPFLkY1V4rMxwCewU3x64RwQ/viewform?usp=sf_link"
            return render_template('result.html', id=utilisateur['ID'], google_form_url=google_form_url)
        else:
            return "Utilisateur non trouvé"
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)