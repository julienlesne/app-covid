import json
from flask import render_template
from werkzeug.wrappers import response
from app import app
import requests
from forms import LoginForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST']) #allows only GET and POST.
def index():

    # Première requête
    url = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=donnees-hospitalieres-covid-19-dep-france%40public&q=&rows=1&refine.date=2021&refine.nom_dep_min=Paris&refine.sex=Tous"
    reponse = requests.get(url)
    data = reponse.json()

    # Requete formulaire
    form = LoginForm()
    if form.validate_on_submit():

        url2 = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=donnees-hospitalieres-covid-19-dep-france%40public&q=&rows=1&refine.date="+form.year.data+"&refine.nom_dep_min=Paris&refine.sex="+form.sexe.data
        new = requests.get(url2)
        data = new.json()

        # Test Graph
        mois = {}
        liste = ["01", "02", "03","04", "05", "06","07", "08", "09","10", "11", "12"]
        for x in liste:
            urltest = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=donnees-hospitalieres-covid-19-dep-france%40public&q=&rows=1&sort=date&refine.nom_dep_min=Paris&refine.sex="+form.sexe.data+"&refine.date="+form.year.data+"%2F"+x
            response2 = requests.get(urltest)
            data2 = response2.json()

            if data2["records"]:
                mois[x] = data2["records"][0]["fields"]["tot_death"]
            else:
                mois[x] = 0
    
        labels = ["Janvier", "Février", "mars","Avril", "Mai", "juin","Juillet", "Août", "Septembre","Octobre", "Novembre", "Décembre"]
        values = [mois[x] for x in liste]

        return render_template('index.html',form=form, tot_death=data["records"][0]["fields"]["tot_death"], tot_out=data["records"][0]["fields"]["tot_out"],
        region_min=data["records"][0]["fields"]["region_min"], nom_dep_min=data["records"][0]["fields"]["nom_dep_min"],
        date=data["records"][0]["fields"]["date"], sex=data["records"][0]["fields"]["sex"],labels=labels, values=values, test = urltest)

    # Test Graph
    mois = {}
    liste = ["01", "02", "03","04", "05", "06","07", "08", "09","10", "11", "12"]
    for x in liste:
        urltest = "https://data.opendatasoft.com/api/records/1.0/search/?dataset=donnees-hospitalieres-covid-19-dep-france%40public&q=&rows=1&sort=date&refine.nom_dep_min=Paris&refine.sex=Tous&refine.date=2020%2F"+x
        response2 = requests.get(urltest)
        data2 = response2.json()

        if data2["records"]:
            mois[x] = data2["records"][0]["fields"]["tot_death"]
        else:
            mois[x] = 0
    
    labels = ["Janvier", "Février", "mars","Avril", "Mai", "juin","Juillet", "Août", "Septembre","Octobre", "Novembre", "Décembre"]
    values = [mois[x] for x in liste]

    # Retour
    return render_template('index.html',form=form, tot_death=data["records"][0]["fields"]["tot_death"], tot_out=data["records"][0]["fields"]["tot_out"],
    region_min=data["records"][0]["fields"]["region_min"], nom_dep_min=data["records"][0]["fields"]["nom_dep_min"],
    date=data["records"][0]["fields"]["date"], sex=data["records"][0]["fields"]["sex"], labels=labels, values=values, test = urltest
    )