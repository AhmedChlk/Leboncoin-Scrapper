import io
import json
import logging
import os
from http.cookies import SimpleCookie
from typing import Optional, Dict
from urllib.parse import urlencode

from curl_cffi import Curl, CurlOpt, CurlInfo, CurlError

COOKIES_PATH = "scrap/data/cookies.json"
DEFAULT_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120 Safari/537.36"
)

class HttpClient:
    def __init__(self, timeout: int = 10, max_retries: int = 3, follow_redirects: bool = True):
        self.timeout = timeout
        self.max_retries = max_retries
        self.follow_redirects = follow_redirects
        self.logger = logging.getLogger("HttpClient")
        self.curl = Curl()
        self.cookies = SimpleCookie()
        self.user_agent = DEFAULT_UA
        self._load_cookies()

    def _load_cookies(self):
        if os.path.exists(COOKIES_PATH):
            try:
                with open(COOKIES_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for k, v in data.items():
                    self.cookies[k] = v
                self.logger.info("Cookies chargés depuis le fichier.")
            except Exception as e:
                self.logger.warning(f"Erreur chargement cookies: {e}")

    def _save_cookies(self):
        try:
            with open(COOKIES_PATH, "w", encoding="utf-8") as f:
                json.dump({k: m.value for k, m in self.cookies.items()}, f, indent=2)
            self.logger.info("Cookies sauvegardés.")
        except Exception as e:
            self.logger.warning(f"Erreur sauvegarde cookies: {e}")

    def _headers_list(self, headers: Optional[Dict[str, str]]) -> list[bytes]:
        final = {"User-Agent": self.user_agent}
        if headers:
            final.update(headers)
        if self.cookies:
            cookie_str = "; ".join(f"{m.key}={m.value}" for m in self.cookies.values())
            final["Cookie"] = cookie_str
        return [f"{k}: {v}".encode() for k, v in final.items()]

    def _update_cookies(self, header_bytes: bytes):
        lines = header_bytes.split(b"\r\n")
        parsed = self.curl.parse_cookie_headers(lines)
        for morsel in parsed.values():
            self.cookies[morsel.key] = morsel.value

    def _request(self, method: str, url: str, *, params=None, data=None, headers=None) -> Optional[str]:
        if params:
            query = urlencode(params, doseq=True)
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}{query}"
        for attempt in range(1, self.max_retries + 1):
            body = io.BytesIO()
            header_buf = io.BytesIO()
            try:
                self.curl.setopt(CurlOpt.URL, url)
                self.curl.setopt(CurlOpt.TIMEOUT, self.timeout)
                self.curl.setopt(CurlOpt.FOLLOWLOCATION, int(self.follow_redirects))
                self.curl.setopt(CurlOpt.WRITEDATA, body)
                self.curl.setopt(CurlOpt.HEADERDATA, header_buf)
                self.curl.setopt(CurlOpt.HTTPHEADER, self._headers_list(headers))
                if method == "POST":
                    self.curl.setopt(CurlOpt.POST, 1)
                    if data is not None:
                        if isinstance(data, str):
                            data = data.encode()
                        self.curl.setopt(CurlOpt.POSTFIELDS, data)
                self.curl.perform()
                status = self.curl.getinfo(CurlInfo.RESPONSE_CODE)
                self._update_cookies(header_buf.getvalue())
                self._save_cookies()
                if 200 <= status < 400:
                    return body.getvalue().decode("utf-8", "ignore")
                self.logger.error(f"Statut {status} pour {url}")
            except CurlError as e:
                self.logger.warning(f"Tentative {attempt} échouée: {e}")
            finally:
                self.curl.reset()
        self.logger.error(f"Echec de la requête {method} {url}")
        return None

    def get(self, url: str, params=None, headers=None) -> Optional[str]:
        return self._request("GET", url, params=params, headers=headers)

    def post(self, url: str, data=None, json_body=None, headers=None) -> Optional[str]:
        if json_body is not None:
            data = json.dumps(json_body)
            headers = headers or {}
            headers.setdefault("Content-Type", "application/json")
        if isinstance(data, dict):
            data = urlencode(data)
        return self._request("POST", url, data=data, headers=headers)
