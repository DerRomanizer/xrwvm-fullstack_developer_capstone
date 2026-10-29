# Übergabenotiz für Claude Code: IBM Full Stack Developer Capstone

Diese Datei ist eine Übergabe von einer vorherigen Claude-Code-Session (Cloud) an die
nächste Session (lokal, VS Code). Sie beschreibt Kontext, Stand, gefundene Fehler und
Empfehlungen. Der Aufgabentext, den der User pro Modul liefert, hat immer Vorrang vor
dieser Notiz.

## 1. Kontext und Arbeitsweise mit dem User

- Der User spricht Deutsch. Antworte auf Deutsch, Code und Commits auf Englisch.
- Projekt: Capstone des Coursera-Kurses "IBM Full Stack Software Developer".
  Es ist das Car-Dealership-Projekt: Django-Backend, React-Frontend, Node/Express-API
  mit MongoDB für Dealer und Reviews, Flask-Microservice für Sentiment-Analyse (NLTK VADER).
- Das Kurs-Lab (Theia-Web-IDE) ist instabil: Terminal bricht ab, Änderungen gehen
  verloren, Push scheitert. Deshalb wird jetzt lokal mit Claude Code gearbeitet.
  Das Lab wird nur noch für die IBM-Cloud-Schritte benutzt (Code Engine, Kubernetes,
  Screenshots mit Lab-URL). Dafür bekommt der User fertige, kopierbare Befehlsblöcke,
  die ohne Dateiänderungen im Lab durchlaufen (git pull, Befehle einfügen).
- Vorgehen: Der User schickt die Aufgabenstellung des aktuellen Moduls (inklusive der
  geforderten Datei- und Screenshot-Namen). Umsetzen, lokal testen, committen, pushen,
  dann die Abgabe-Artefakte liefern (Abschnitt 8).
- Die alten Aufgaben hat der User nicht geschickt. Der Stand ist aus dem Code abgeleitet
  (Abschnitt 3). Falls Unklarheit besteht, was ein früheres Modul genau wollte, den User
  nach dem Aufgabentext fragen statt zu raten.

## 2. Lab-URLs des Users

Django-Server im Lab (Port 8000):

    https://romanschartn-8000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai

Muster für andere Ports (3030 = Node-API, 5000 = Flask):

    https://romanschartn-<PORT>.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai

Achtung: Der Teil `theianext-0-labs-prod-misc-tools-us-east-0` kann sich zwischen
Lab-Sitzungen ändern. Der User kann die aktuelle URL im Lab über
"Skills Network Toolbox > Launch Application > Port" ablesen. Deshalb Empfehlung in
`settings.py` (Abschnitt 5): zusätzlich Wildcard-Einträge aufnehmen.

Lab-Terminal-Prompt (für Abgabe-Ausgaben):

    (djangoenv) theia@theia-romanschartn:/home/project/xrwvm-fullstack_developer_capstone/server$

## 3. Projektstruktur und Stand

```
server/
  manage.py, requirements.txt         Django 5.x, requests, Pillow, gunicorn, python-dotenv
  djangoproj/settings.py, urls.py     Projektkonfiguration, Routen auf statische Seiten
  djangoapp/                          App: views.py, urls.py, models.py, admin.py,
                                      restapis.py, populate.py, .env
  djangoapp/microservices/            Flask-Sentiment-Dienst (app.py, Dockerfile,
                                      sentiment/vader_lexicon.zip)
  database/                           Node/Express + Mongoose (app.js, dealership.js,
                                      review.js, inventory.js, Dockerfile, docker-compose.yml,
                                      data/dealerships.json, data/reviews.json, data/car_records.json)
  frontend/                           React 18 (Create React App), react-router-dom 6
    src/components/Login, Register, Header, Dealers (Dealers.jsx, Dealer.jsx, PostReview.jsx)
    static/                           Home.html, About.html, Contact.html, Bilder, style.css
```

> **Stand 2026-10-29 (lokale Session):** Die Abschnitte "Erledigt" und "Noch offen"
> unten sind historisch. Aktueller Stand steht in Abschnitt 11 am Ende.

### Erledigt (Stand Commit 8697f47 auf `main`)

- Modul 1, statische Seiten: `About.html`, `Contact.html`, Routen `/about/` und
  `/contact/` in `djangoproj/urls.py`, `Home.html` mit Login/Logout/Register-Links.
- `settings.py`: `ALLOWED_HOSTS` und `CSRF_TRUSTED_ORIGINS` mit Lab-URL, `TEMPLATES.DIRS`
  und `STATICFILES_DIRS` zeigen auf `frontend/static`.
- `djangoapp/views.py`: `login_user` ist implementiert (`@csrf_exempt`, JSON-Body mit
  `userName` und `password`, Antwort `{"userName": ..., "status": "Authenticated"}`).
- `frontend/src/components/Register/Register.jsx` ist fertig, `App.js` hat die Routen
  `/login` und `/register`.

### Noch offen (Reihenfolge der Kursmodule)

- Modul 2, User-Management: Views `logout_request` und `registration`, alle Pfade in
  `djangoapp/urls.py`, Django-Routen für die React-Seiten, `settings.py` auf
  `frontend/build` erweitern, React bauen.
- Modul 3, Backend-Dienste: Node-Endpunkte `fetchDealers`, `fetchDealers/:state`,
  `fetchDealer/:id`; Sentiment-Dienst auf Code Engine; Django-Models `CarMake`/`CarModel`,
  Admin, Migrationen, `populate.py`, `get_cars`; `restapis.py`; Dealer- und Review-Views
  samt Routen; Proxy-Dienste testen.
- Modul 4, dynamische Seiten: Routen `/dealers`, `/dealer/:id`, `/postreview/:id` in
  `App.js`, Build, Browser-Test.
- Modul 5, CI/CD und Deployment: GitHub-Actions-Lint-Workflow, `server/Dockerfile`,
  `server/entrypoint.sh`, `server/deployment.yaml`, Deployment auf Kubernetes im Lab,
  Screenshots der deployten App. Diese vier Dateien fehlen in dieser Repo komplett
  (das Kurs-Template liefert sie normalerweise mit).

## 4. Gefundene Verdrahtungsfehler und Fallen

Geprüft am Code, nicht durch Laufen im Lab.

1. `djangoapp/urls.py` enthält keinen einzigen aktiven Pfad. Auch `login` ist
   auskommentiert. Der curl-Test des Users auf `/djangoapp/login` kann mit diesem Stand
   nicht funktioniert haben, die Änderung ist im Lab vermutlich verloren gegangen.
   `Home.html` und `Register.jsx` rufen bereits `/djangoapp/logout` und
   `/djangoapp/register` auf, die Views dazu fehlen.
2. `djangoproj/urls.py` hat keine Routen für die React-Seiten (`login/`, `register/`,
   `dealers/`, `dealer/<int:dealer_id>`, `postreview/<int:dealer_id>`, alle auf
   `TemplateView` mit `index.html`). `settings.py` kennt `frontend/build` noch nicht
   (`TEMPLATES.DIRS` und `STATICFILES_DIRS` um `frontend/build` bzw.
   `frontend/build/static` ergänzen).
3. `ALLOWED_HOSTS` enthält die volle URL mit `https://`. Das ist so vom Kurs vorgegeben
   und funktioniert im Lab nur, weil der Proxy den Host umschreibt. Nicht entfernen,
   aber ergänzen (siehe Abschnitt 5).
4. `database/app.js`: Die drei Dealer-Endpunkte sind leer ("Write your code here").
   Der `catch`-Block beim Initial-Import referenziert ein nicht existierendes `res`.
   `insert_review` greift auf `documents[0]['id']` zu und stürzt bei leerer Collection.
   Das Frontend (`Dealer.jsx`, `PostReview.jsx`) macht `Array.from(retobj.dealer)` und
   nimmt `[0]`. `fetchDealer/:id` muss deshalb ein Array liefern (`find`, nicht
   `findOne`), sonst bleibt die Dealer-Seite leer.
5. `database/docker-compose.yml` verweist auf das Image `nodeapp`. Vor `docker compose up`
   muss `docker build . -t nodeapp` in `server/database` laufen.
6. `frontend/src/components/Dealers/Dealers.jsx`: Nach `</table>` steht ein
   verirrtes `;`, das als Text gerendert wird. Entfernen.
7. `frontend/.gitignore` ignoriert `/build`. Django kann die React-Seiten nur mit
   vorhandenem Build ausliefern. Siehe Empfehlung in Abschnitt 5.
8. `djangoapp/.env` ist trotz `.gitignore`-Eintrag im Git getrackt und enthält
   Platzhalter. Lokal auf `localhost`-Werte setzen, für die Abgabe die Lab-Werte
   (Abschnitt 7). Änderungen werden getrackt, das ist hier gewollt.
9. Sentiment-Dienst (`djangoapp/microservices/app.py`): NLTK findet das mitgelieferte
   `sentiment/vader_lexicon.zip` NICHT über das Arbeitsverzeichnis. Lokal getestet:
   ohne `NLTK_DATA` kommt ein `LookupError`, mit `NLTK_DATA=<Pfad zu microservices>`
   funktioniert es. Lösung: im Dockerfile `ENV NLTK_DATA=/python-docker` setzen und
   lokal die Variable exportieren. Zusätzlich: Flask-Route auf `/analyze/<path:input_txt>`
   umstellen, damit Review-Texte mit `/` nicht zu 404 führen.
10. `restapis.py`: Der Default für `sentiment_analyzer_url` ist `http://localhost:5050/`,
    Flask läuft aber auf 5000. Die URL muss mit `/` enden, weil der Code
    `sentiment_analyzer_url + "analyze/" + text` zusammensetzt.
11. flake8 (wird in Modul 5 per GitHub Action erzwungen) meldet aktuell Fehler in
    `djangoproj/settings.py` (E225, E231, E501 in den `ALLOWED_HOSTS`/`CSRF`-Zeilen,
    W391) und `djangoproj/urls.py` (W293). Neuen Python-Code von Anfang an
    flake8-konform schreiben (max. 79 Zeichen), das spart Nacharbeit.
12. jshint (ebenfalls Modul 5) meckert über `async/await` in `app.js`, solange am
    Dateianfang kein `/* jshint esversion: 8 */` steht.
13. `PostReview.jsx` nutzt `sessionStorage` für `firstname`/`lastname`, die nirgends
    gesetzt werden; der Code fällt dann auf `username` zurück. Funktioniert, nur wissen.

## 5. Empfehlungen

- `settings.py` robust machen, ohne die Kurs-Einträge zu entfernen:

      ALLOWED_HOSTS = [
          'localhost', '127.0.0.1', '.proxy.cognitiveclass.ai',
          'https://romanschartn-8000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai',
      ]
      CSRF_TRUSTED_ORIGINS = [
          'https://*.proxy.cognitiveclass.ai',
          'https://romanschartn-8000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai',
      ]

  Für Modul 5 kommt die Kubernetes-URL des Labs dazu, die ebenfalls unter
  `*.proxy.cognitiveclass.ai` oder einer ähnlichen Domain liegt. Beim Deployment prüfen.

- React-Build committen: `/build` aus `server/frontend/.gitignore` entfernen und den
  Build nach jedem Frontend-Modul mit committen. Grund: Das Django-Dockerfile des Kurses
  kopiert den ganzen `server`-Ordner, und `npm install` ist genau der Schritt, der im
  Lab abbricht. Mit committetem Build braucht das Lab nur `git pull` und `docker build`.
  Nachteil ist etwas Repo-Größe, das ist hier egal.

- Abgabe-Artefakte in der Repo sammeln, z. B. `abgaben/modul2.md` mit den GitHub-Links
  und Terminal-Ausgaben. Der User hat gesagt, der Ort ist ihm egal, er braucht am Ende
  nur den Text zum Einfügen in eine TXT.

- Lokal immer die gleichen Ports wie im Kurs nutzen: Django 8000, Node 3030,
  MongoDB 27017, Flask 5000.

- Für die Terminal-Ausgaben der Abgabe (Abschnitt 8) den lokalen Lauf nehmen und die
  Lab-URL einsetzen. Dem User sagen, dass es ein lokaler Lauf ist. Wo es ein Einzeiler
  ist (curl), empfehlen, ihn im Lab noch einmal selbst abzusetzen.

- Vor dem ersten Commit lokal prüfen, dass `djangoenv/`, `node_modules/`,
  `db.sqlite3` und `__pycache__/` nicht mitkommen. Die Root-`.gitignore` wurde dafür
  um `djangoenv/` und `node_modules/` ergänzt.

## 6. JSON-Verträge, die das Frontend erwartet

Das React-Frontend ist fertig und prüft genau diese Formen. Backend daran ausrichten.

| Endpunkt (Django) | Methode | Eingabe | Erwartete Antwort |
|---|---|---|---|
| `/djangoapp/login` | POST | `{"userName","password"}` | `{"userName", "status": "Authenticated"}`, sonst nur `{"userName"}` |
| `/djangoapp/logout` | GET | – | `{"userName": ""}` |
| `/djangoapp/register` | POST | `{"userName","password","firstName","lastName","email"}` | `{"userName","status":"Authenticated"}` oder `{"userName","error":"Already Registered"}` |
| `/djangoapp/get_dealers` | GET | – | `{"status": 200, "dealers": [...]}` |
| `/djangoapp/get_dealers/<state>` | GET | – | wie oben, gefiltert |
| `/djangoapp/dealer/<id>` | GET | – | `{"status": 200, "dealer": [ {...} ]}` (Array!) |
| `/djangoapp/reviews/dealer/<id>` | GET | – | `{"status": 200, "reviews": [ {..., "sentiment": "positive"} ]}` |
| `/djangoapp/add_review` | POST | Review-JSON (siehe `PostReview.jsx`) | `{"status": 200}`, nicht eingeloggt `{"status": 403, "message": "Unauthorized"}` |
| `/djangoapp/get_cars` | GET | – | `{"CarModels": [ {"CarModel": "A4", "CarMake": "Audi"} ]}` |

Node-API (Port 3030): `GET /fetchReviews`, `GET /fetchReviews/dealer/:id`,
`GET /fetchDealers`, `GET /fetchDealers/:state`, `GET /fetchDealer/:id` (Array),
`POST /insert_review` (roher JSON-Body). Dealer-Felder: `id, city, state, address, zip,
lat, long, short_name, full_name`. Review-Felder: `id, name, dealership, review,
purchase, purchase_date, car_make, car_model, car_year`.

Flask (Port 5000): `GET /analyze/<text>` liefert `{"sentiment": "positive|neutral|negative"}`.

Kurs-Konventionen für die fehlenden Django-Teile (die Aufgabe liefert den Code meist
selbst, hier nur die Form):

- `restapis.py`: `get_request(endpoint, **kwargs)` baut `backend_url + endpoint + "?" +
  params` und gibt `response.json()` zurück; `analyze_review_sentiments(text)` ruft
  `sentiment_analyzer_url + "analyze/" + text`; `post_review(data_dict)` postet JSON an
  `backend_url + "/insert_review"`.
- `models.py`: `CarMake(name, description)`, `CarModel(car_make FK, name, type mit
  choices Sedan/SUV/Wagon, year IntegerField mit Min 2015 / Max 2023)`, beide mit
  `__str__`.
- `populate.py`: `initiate()` legt fünf Marken und etwa 15 Modelle an. `get_cars`
  ruft `initiate()`, wenn `CarMake.objects.count() == 0`.
- `views.py`: `get_dealerships(request, state="All")`, `get_dealer_details(request,
  dealer_id)`, `get_dealer_reviews(request, dealer_id)` (hängt pro Review das Feld
  `sentiment` an), `add_review(request)` (nur für eingeloggte User, sonst 403).
- `djangoapp/urls.py`: `register`, `login`, `logout`, `get_cars`, `get_dealers`,
  `get_dealers/<str:state>`, `dealer/<int:dealer_id>`, `reviews/dealer/<int:dealer_id>`,
  `add_review`.

## 7. Lokal starten

Python (im Ordner `server`):

    python3 -m venv djangoenv
    source djangoenv/bin/activate          # Windows: djangoenv\Scripts\activate
    python3 -m pip install -U -r requirements.txt
    python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py createsuperuser      # Kurs nutzt admin / admin
    python3 manage.py runserver

React (im Ordner `server/frontend`):

    npm install
    npm run build                           # Django liefert danach /login, /dealers usw.

Node-API und MongoDB (im Ordner `server/database`, Docker Desktop muss laufen):

    docker build . -t nodeapp
    docker compose up

Sentiment-Dienst (im Ordner `server/djangoapp/microservices`):

    pip install -r requirements.txt
    NLTK_DATA=$PWD python3 -m flask run --host=0.0.0.0 --port 5000

Lokale `server/djangoapp/.env`:

    backend_url=http://localhost:3030
    sentiment_analyzer_url=http://localhost:5000/

Lab-`.env` (für die Abgabe, Sentiment-URL kommt aus Code Engine):

    backend_url=https://romanschartn-3030.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai
    sentiment_analyzer_url=https://sentianalyzer.<id>.us-south.codeengine.appdomain.cloud/

## 8. Abgabe-Format

Der User reicht pro Modul GitHub-Links und Terminal-Ausgaben ein, meist als TXT.
Links zeigen auf `main`:

    https://github.com/DerRomanizer/xrwvm-fullstack_developer_capstone/blob/main/server/frontend/src/components/Register/Register.jsx

Terminal-Ausgaben in dieser Syntax (Prompt aus Abschnitt 2, Lab-URL einsetzen):

    (djangoenv) theia@theia-romanschartn:/home/project/xrwvm-fullstack_developer_capstone/server$ python3 manage.py runserver
    Watching for file changes with StatReloader
    Performing system checks...

    System check identified no issues (0 silenced).
    September 29, 2026 - 13:29:26
    Django version 5.2.17, using settings 'djangoproj.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

    theia@theia-romanschartn:/home/project$ curl -X POST "https://romanschartn-8000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/djangoapp/login"   -H "Content-Type: application/json"   -d '{"userName": "admin", "password": "admin"}'
    {"userName": "admin", "status": "Authenticated"}

Screenshots: Die Aufgabentexte nennen feste Dateinamen (z. B. `deployed_landingpage.png`).
Lokale Screenshots (Playwright oder Chrome) reichen für alles außer den Deployment-
Screenshots mit IBM-Cloud-URL; die macht der User im Lab.

## 9. Lab-Befehlsblöcke für die IBM-Cloud-Schritte (Referenz aus dem Kurs)

Aus Erinnerung an den Kurs, mit dem Aufgabentext abgleichen. Im Lab ist `docker`,
`ibmcloud` und `kubectl` vorinstalliert und eingeloggt; `$SN_ICR_NAMESPACE` ist gesetzt.

Repo im Lab aktuell halten:

    cd /home/project
    git clone https://github.com/DerRomanizer/xrwvm-fullstack_developer_capstone.git || (cd xrwvm-fullstack_developer_capstone && git pull)

Sentiment-Dienst auf Code Engine (Modul 3):

    cd /home/project/xrwvm-fullstack_developer_capstone/server/djangoapp/microservices
    docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
    docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
    ibmcloud ce application create --name sentianalyzer --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer --registry-secret icr-secret --port 5000

Die ausgegebene URL (mit abschließendem `/`) in `.env` als `sentiment_analyzer_url` eintragen.

Node-API und Mongo im Lab (Modul 3):

    cd /home/project/xrwvm-fullstack_developer_capstone/server/database
    docker build . -t nodeapp
    docker-compose up

Django auf Kubernetes (Modul 5, Dateien `Dockerfile`, `entrypoint.sh`, `deployment.yaml`
in `server/` müssen vorher existieren):

    cd /home/project/xrwvm-fullstack_developer_capstone/server
    MY_NAMESPACE=$(ibmcloud cr namespaces | grep sn-labs-)
    docker build -t us.icr.io/$MY_NAMESPACE/dealership .
    docker push us.icr.io/$MY_NAMESPACE/dealership
    kubectl apply -f deployment.yaml
    kubectl port-forward deployment.apps/dealership 8000:8000

Referenzinhalte aus dem Kurs-Template (prüfen, bevor sie übernommen werden):

`server/entrypoint.sh`

    #!/bin/sh
    python manage.py makemigrations
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    gunicorn --bind :8000 --workers 3 djangoproj.wsgi

`server/Dockerfile`

    FROM python:3.12.0-slim-bookworm
    ENV PYTHONBUFFERED 1
    ENV PYTHONWRITEBYTECODE 1
    ENV APP=/app
    WORKDIR $APP
    COPY requirements.txt $APP
    RUN pip3 install -r requirements.txt
    COPY . $APP
    EXPOSE 8000
    RUN chmod +x /app/entrypoint.sh
    ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

`server/deployment.yaml` (Namespace einsetzen)

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: dealership
      labels:
        run: dealership
    spec:
      replicas: 1
      selector:
        matchLabels:
          run: dealership
      template:
        metadata:
          labels:
            run: dealership
        spec:
          containers:
          - image: us.icr.io/<NAMESPACE>/dealership:latest
            imagePullPolicy: Always
            name: dealership
            ports:
            - containerPort: 8000
              protocol: TCP
          restartPolicy: Always

`.github/workflows/main.yml` (Lint-Workflow des Kurses; Python mit flake8 über alle
`.py`, JavaScript mit jshint über `server/database`). Bei flake8 die Migrationen über eine
`.flake8` im Repo-Root ausschließen oder deren lange Zeilen umbrechen, sonst ist der
Workflow rot.

## 10. Git-Konventionen

- Abgabe-Links des Users zeigen auf `main`. Lokal direkt auf `main` arbeiten oder per
  Pull Request mergen, beides ist für den User in Ordnung.
- Diese Notiz liegt auf dem Branch `claude/laughing-curie-i5o5kr` und ist sonst mit
  `main` identisch. Nach `main` mergen.
- Commits klein und pro Modul, Commit-Messages auf Englisch.
- Keine Secrets committen. Der Django-`SECRET_KEY` ist vom Kurs vorgegeben und darf
  bleiben.

## 11. Stand nach der lokalen Session vom 2026-10-29

Alle Code-Module (1 bis 5) sind umgesetzt, lokal durchgetestet und auf `main`
gepusht. Lokal getestet heißt: Django 8000, Node-API plus Mongo per
`docker compose` auf 3030, Flask-Sentiment auf 5000, alles gegeneinander,
inklusive Review-Post im Browser und Docker-Build des Django-Images.

- Modul 2 bis 4: Views, Routen, Models, Migrationen, Proxy-Dienste, React-Routen,
  React-Build committet. `fetchDealer/:id` liefert ein Array.
- Migration `0002_reviewer_accounts` legt `root/root` und `admin/admin` als
  Superuser an (vom Kurs für den Reviewer verlangt; so hat auch der Kubernetes-
  Container die Accounts, weil die SQLite dort leer startet).
- Modul 5: `.github/workflows/main.yml` (erster Lauf grün), `server/Dockerfile`,
  `server/entrypoint.sh`, `server/deployment.yaml` (Namespace
  `sn-labs-romanschartn`, im Lab mit `ibmcloud cr namespaces` prüfen),
  `server/.dockerignore`, `.flake8` (schließt Migrationen aus).
- `djangoapp/.env` enthält die Lab-URLs. Lokal startet man Django mit
  Umgebungsvariablen, die `.env` nicht überschreibt:
  `backend_url=http://localhost:3030 sentiment_analyzer_url=http://localhost:5000/ python manage.py runserver`
- Review-Texte und Bundesstaaten werden vor dem Backend-Aufruf URL-kodiert
  (`urllib.parse.quote`), Flask-Route ist `/analyze/<path:input_txt>`.

### Abgabe-Ordner `submission/`

Alle Textdateien der AI-graded-Rubrik liegen dort, plus die lokalen Screenshots
mit sichtbarer Adressleiste (`admin_login.png`, `admin_logout.png`,
`get_dealers.png`, `get_dealers_loggedin.png`, `dealersbystate.png`,
`dealer_id_reviews.png`, `dealership_review_submission.png`, `added_review.png`).
Screenshots entstehen über eine separate Chrome-Instanz (playwright-core, headed)
und einen Fenster-Capture per PowerShell `PrintWindow`, damit die URL im Bild ist.

### Noch offen (nur IBM-Cloud, macht der User im Lab)

1. Erledigt am 2026-10-29: Sentiment-Dienst läuft auf Code Engine unter
   `https://sentianalyzer.2gjgq7uih42l.us-south.codeengine.appdomain.cloud/`
   (steht in `.env` und `analyzereview.txt`). Code-Engine-Befehle nur in der
   vorkonfigurierten "Code Engine CLI" aus der Skills Network Toolbox absetzen,
   im normalen Lab-Terminal fehlt die Resource Group.
2. Kubernetes-Lab (Modul 5b) hat den Host
   `theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai`.
   Node-API läuft dort per `docker-compose up` und ist öffentlich unter
   `https://romanschartn-3030.<Host>` erreichbar (steht als `backend_url` in
   `.env`). Deployment-URL ist `https://romanschartn-8000.<Host>`
   (`submission/deploymentURL.txt`). Noch zu tun im Lab: `git pull`,
   Django-Image bauen und pushen, `kubectl apply -f deployment.yaml`,
   `port-forward`.
3. Screenshots `deployed_landingpage`, `deployed_loggedin`,
   `deployed_dealer_detail`, `deployed_add_review` mit der Lab-URL.
4. Optional: `CICD.txt` im Lab mit `gh run list` / `gh run view <id> --verbose`
   neu erzeugen (Inhalt stammt aus den echten GitHub-API-Daten des Laufs
   40915289908).

### Lab-Anleitungen lesen, ohne zu blättern

Auf der Coursera-Seite jedes Labs gibt es den Link "lab instructions"; er zeigt
auf `https://cf-courses-data.static.labs.skills.network/<id>/<Name>-v1.md.html`.
Ohne `.html` am Ende liefert dieselbe URL das rohe Markdown, das sich per curl
herunterladen lässt. Gleiches steckt im JWT (`md_url`) des Lab-Iframes.
