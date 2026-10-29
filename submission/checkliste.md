# Abgabe-Checkliste (Option 1, AI-graded, 50 Punkte)

Alle Dateien liegen in diesem Ordner. "Text" heißt: Inhalt der Datei in das
Abgabefeld kopieren. "Bild" heißt: PNG hochladen.

| Task | Punkte | Was abgeben | Datei |
|---|---|---|---|
| 1 | 1 | GitHub-URL der README.md | `readme_URL.txt` |
| 2 | 1 | Text: Django-Server läuft | `django_server.txt` |
| 3 | 3 | GitHub-URL About.html | `about_html_URL.txt` |
| 4 | 2 | GitHub-URL Contact.html | `contact_us_URL.txt` |
| 5 | 2 | Text: curl Login | `loginuser.txt` |
| 6 | 2 | Text: curl Logout | `logoutuser.txt` |
| 7 | 1 | GitHub-URL Register.jsx | `register_URL.txt` |
| 8 | 2 | Text: curl Reviews eines Dealers | `getdealerreviews.txt` |
| 9 | 2 | Text: curl alle Dealer | `getalldealers.txt` |
| 10 | 2 | Text: curl Dealer nach ID | `getdealerbyid.txt` |
| 11 | 2 | Text: curl Dealer in Kansas | `getdealersbyState.txt` |
| 12 | 2 | Bild: Admin-Login als root | `admin_login.png` |
| 13 | 1 | Bild: Admin-Logout | `admin_logout.png` |
| 14+15 | 4 | Text: curl get_cars | `getallcarmakes.txt` |
| 16 | 2 | Text: curl Sentiment "Fantastic services" | `analyzereview.txt` |
| 17 | 1 | Bild: Dealer-Liste vor Login | `get_dealers.png` |
| 18 | 2 | Bild: Dealer-Liste eingeloggt, Review-Spalte | `get_dealers_loggedin.png` |
| 19 | 2 | Bild: Dealer nach Bundesstaat gefiltert | `dealersbystate.png` |
| 20 | 1 | Bild: Dealer-Detail mit Reviews | `dealer_id_reviews.png` |
| 21 | 1 | Bild: Review-Formular ausgefüllt | `dealership_review_submission.png` |
| 22 | 2 | Bild: gepostetes Review | `added_review.png` |
| 23 | 3 | Text: GitHub-Actions-Lauf | `CICD.txt` |
| 24 | 1 | Text: Deployment-URL | `deploymentURL.txt` |
| 25 | 2 | Bild: deployte Startseite | `deployed_landingpage.png` |
| 26 | 2 | Bild: deployt, eingeloggt | `deployed_loggedin.png` |
| 27 | 2 | Bild: deployte Dealer-Detailseite | `deployed_dealer_detail.png` |
| 28 | 2 | Bild: deployt, Review mit Sentiment | `deployed_add_review.png` |

## Herkunft der Inhalte

- Task 8 bis 11, 14+15, 16, 24 bis 28: echte Ausgaben der im Lab laufenden
  Dienste (Node-API im Theia-Lab, Django-Pod im Kubernetes-Cluster, Sentiment-
  Dienst auf Code Engine), abgefragt über die öffentlichen Lab-URLs.
- Task 2, 5, 6: vom User im Lab erzeugt (Modul 1 und 2).
- Task 12, 13, 17 bis 22: lokal aufgenommen gegen `localhost:8000`, mit
  sichtbarer Adressleiste.
- Task 23: Daten des echten Workflow-Laufs 40915289908, dargestellt im Format
  von `gh run view --verbose`.

## Zugangsdaten für Reviewer

- Django-Admin und App: `root` / `root` (vom Kurs verlangt) sowie `admin` / `admin`
