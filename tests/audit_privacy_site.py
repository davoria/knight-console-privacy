#!/usr/bin/env python3
"""Contrôles statiques, sans dépendance, du site fourni à l'audit."""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PAGES = (ROOT / "index.html", ROOT / "delete-account.html")


class SurfaceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.scripts = 0
        self.forms = 0
        self.remote_resources: list[str] = []
        self.links: list[str] = []
        self.inline_handlers: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "script":
            self.scripts += 1
        if tag == "form":
            self.forms += 1
        for name, value in attrs:
            if name.lower().startswith("on"):
                self.inline_handlers.append(name)
            if value and name in {"src", "href"} and value.startswith(("http://", "https://", "//")):
                self.remote_resources.append(value)
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    parsed: dict[str, SurfaceParser] = {}
    for page in PAGES:
        if not page.is_file():
            fail(f"page absente: {page.relative_to(ROOT)}")
        text = page.read_text(encoding="utf-8")
        parser = SurfaceParser()
        parser.feed(text)
        parser.close()
        parsed[page.name] = parser
        if parser.scripts:
            fail(f"{page.name}: {parser.scripts} script(s) inattendu(s)")
        if parser.forms:
            fail(f"{page.name}: {parser.forms} formulaire(s) inattendu(s)")
        if parser.remote_resources:
            fail(f"{page.name}: ressources distantes: {parser.remote_resources}")
        if parser.inline_handlers:
            fail(f"{page.name}: gestionnaires inline: {parser.inline_handlers}")

    index_text = PAGES[0].read_text(encoding="utf-8")
    deletion_text = PAGES[1].read_text(encoding="utf-8")
    required_index = ("Firebase Authentication", "Cloud Firestore", "8 secondes")
    required_deletion = ("Firebase Authentication", "8 secondes", "irréversible")
    for marker in required_index:
        if marker not in index_text:
            fail(f"index.html: mention attendue absente: {marker}")
    for marker in required_deletion:
        if marker not in deletion_text:
            fail(f"delete-account.html: mention attendue absente: {marker}")

    if "./delete-account.html" not in parsed["index.html"].links:
        fail("index.html: lien vers la procédure de suppression absent")
    if "./" not in parsed["delete-account.html"].links:
        fail("delete-account.html: lien de retour vers la politique absent")
    if not any(link.startswith("mailto:") for link in parsed["delete-account.html"].links):
        fail("delete-account.html: contact de suppression absent")

    tracked_text = "\n".join(page.read_text(encoding="utf-8") for page in PAGES)
    secret_markers = (
        r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r'"type"\s*:\s*"service_account"',
        r"AIza[0-9A-Za-z_-]{35}",
        r"gh[opsu]_[0-9A-Za-z]{20,}",
    )
    for pattern in secret_markers:
        if re.search(pattern, tracked_text):
            fail("motif de secret potentiel détecté (valeur volontairement masquée)")

    print("PASS: 2 pages analysées; aucune surface script/formulaire/ressource distante")
    print("PASS: liens et déclarations critiques cohérents")
    print("PASS: aucun motif de secret courant détecté dans les pages")


if __name__ == "__main__":
    main()
