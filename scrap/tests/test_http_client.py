from scrap.infra.http_client import HttpClient

def test_homepage_leboncoin():
    client = HttpClient()
    url = "https://www.leboncoin.fr/ad/voitures/2997258439"
    html = client.get(url)
    if html:
        print("✅ Requête réussie.")
        print(html[:500])
    else:
        print("❌ Échec de la requête.")
