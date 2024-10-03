from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

# Chargez le fichier CSV dans un dictionnaire
def lire_base_donnees():
    base_donnees = []
    with open('basse_donnees.csv', newline='', encoding='utf-8') as csvfile:
        lecteur_csv = csv.DictReader(csvfile)
        for ligne in lecteur_csv:
            base_donnees.append(ligne)
    return base_donnees

# Fonction pour vérifier si le numéro a déjà voté
def a_deja_vote(numero):
    if not os.path.exists('votants.csv'):
        # Si le fichier votants.csv n'existe pas, cela signifie qu'aucun vote n'a encore été enregistré
        return False
    with open('votants.csv', newline='', encoding='utf-8') as csvfile:
        lecteur_csv = csv.reader(csvfile)
        for ligne in lecteur_csv:
            if ligne[0] == numero:
                return True
    return False

# Fonction pour enregistrer un numéro après un vote
def enregistrer_vote(numero):
    with open('votants.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([numero])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        numero = request.form['numero']

        # Vérifier si l'utilisateur a déjà voté
        if a_deja_vote(numero):
            return "لقد قمت بالتصويت بالفعل. لا يُسمح بالتصويت أكثر من مرة."

        # Chercher l'utilisateur dans la base de données uniquement par numéro de téléphone
        base_donnees = lire_base_donnees()
        utilisateur = next((u for u in base_donnees if u['Numéro téléphone'] == numero), None)

        if utilisateur:
            # ID utilisateur trouvé, on affiche le lien du formulaire Google
            google_form_url = f"https://docs.google.com/forms/d/e/1FAIpQLSfac4EIrtXxHmgQfGbe2RiHb0JPFLkY1V4rMxwCewU3x64RwQ/viewform?usp=pp_url&entry.132131935={utilisateur['ID']}"

            # Enregistrer que cet utilisateur a voté
            enregistrer_vote(numero)

            return render_template('result.html', id=utilisateur['ID'], google_form_url=google_form_url)
        else:
            return "المستخدم غير موجود"

    return render_template('index.html')

if __name__ == '__main__':
    app.run
