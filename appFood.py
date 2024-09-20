from flask import Flask, render_template, redirect, url_for
import csv

app = Flask(__name__)#, template_folder='.')
file_path = 'static/listedescollabsetmenus.csv'

import os
current_folder = os.getcwd()

@app.route("/")
def helloWorld():
    return "Hello World"


@app.route("/reservermonplat")
def afficherHomePage():
    ligneFichierCSV = restituerCSV()
    return render_template("index.html", data=ligneFichierCSV)


@app.route("/reservermonplat/add")
def pageAjouterPersonne():
    ligneFichierCSV = restituerCSV()
    return render_template('ajout.html', data=ligneFichierCSV)

@app.route("/reservermonplat/Modifier<indexPersonne>")
def modifierRestaurantMenu(indexPersonne):
    ligneFichierCSV = restituerCSV()
    return render_template('modification.html', data=ligneFichierCSV, champsAmodifier=int(indexPersonne))

@app.route("/reservermonplat/add/<nom>/<restaurant>/<menu>")
def validerAjoutNomRestaurantMenu(nom,restaurant,menu):
    ligneFichierCSV = restituerCSV()
    ligneFichierCSV.append([nom,restaurant,menu])
    miseAjourCSV(ligneFichierCSV)
    return redirect(url_for('afficherHomePage'))  # Rediriger vers la page d'accueil après la modification

@app.route("/reservermonplat/<numLigne>/<restaurant>/<menu>")
def validerModificationRestaurantMenu(numLigne, restaurant, menu):
    numLigne = int(numLigne)
    ligneFichierCSV = restituerCSV()
    ligneFichierCSV[numLigne][1] = restaurant
    ligneFichierCSV[numLigne][2] = menu
    miseAjourCSV(ligneFichierCSV)
    return redirect(url_for('afficherHomePage'))  # Rediriger vers la page d'accueil après la modification

@app.route("/reservermonplat/supprimer/<int:rowIndex>")
def supprimerPersonne(rowIndex):
    ligneFichierCSV = restituerCSV()
    if 0 <= rowIndex < len(ligneFichierCSV):
        del ligneFichierCSV[rowIndex]
        miseAjourCSV(ligneFichierCSV)
    return '', 204  # Indiquer que la suppression a été réussie

def miseAjourCSV(monFichierCSV):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(monFichierCSV)

def restituerCSV():
    with open(file_path, newline='') as csvfile:
        listeCommandes = csv.reader(csvfile, delimiter=';')
        ligneFichierCSV = [row for row in listeCommandes]
        return ligneFichierCSV
