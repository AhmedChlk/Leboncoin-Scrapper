from scrap.infra.http_client import HttpClient
client = HttpClient()
for c in cookies:
    client.cookies[c["name"]] = c["value"]

text = client.get("https://www.leboncoin.fr/account/private/home")
print("✅ Contenu partiel:", text[:200] if text else "Erreur")
