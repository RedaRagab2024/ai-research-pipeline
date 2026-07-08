import os
import time
import requests
from Bio import Entrez
from typing import Dict, Any, List

Entrez.email = os.getenv("ENTREZ_EMAIL", "you@example.com")
CROSSREF_BASE = "https://api.crossref.org/works/"

def search_pubmed(query: str, max_results=50) -> List[str]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    pmids = record.get("IdList", [])
    return pmids

def fetch_pubmed_metadata(pmids: List[str]) -> List[Dict[str, Any]]:
    out = []
    if not pmids:
        return out
    handle = Entrez.efetch(db="pubmed", id=",".join(pmids), rettype="xml")
    records = Entrez.read(handle)
    handle.close()
    for rec in records.get('PubmedArticle', []):
        art = rec.get('MedlineCitation', {}).get('Article', {})
        title = art.get('ArticleTitle')
        doi = None
        try:
            for id_item in rec.get('PubmedData', {}).get('ArticleIdList', []):
                if getattr(id_item, 'attributes', None) and id_item.attributes.get('IdType') == 'doi':
                    doi = str(id_item)
                else:
                    if isinstance(id_item, dict) and id_item.get('IdType') == 'doi':
                        doi = id_item.get('_') or id_item.get('value')
        except Exception:
            doi = None
        out.append({"title": title, "doi": doi, "raw": rec})
    return out

def verify_doi(doi: str):
    if not doi:
        return False, None
    url = CROSSREF_BASE + requests.utils.quote(doi)
    try:
        r = requests.get(url, timeout=10)
    except Exception:
        return False, None
    if r.status_code == 200:
        data = r.json().get("message")
        return True, data
    return False, None

def run(state_obj, query: str):
    pmids = search_pubmed(query)
    items = fetch_pubmed_metadata(pmids)
    verified = []
    for item in items:
        doi = item.get("doi")
        ok, meta = verify_doi(doi) if doi else (False, None)
        entry = {
            "title": item.get("title"),
            "pmid": None,
            "doi": doi,
            "doi_verified": ok,
            "crossref_meta": meta,
            "source": "pubmed"
        }
        verified.append(entry)
        time.sleep(0.1)
    cur_bib = state_obj.get("verified_bibliography", []) or []
    cur_bib.extend(verified)
    state_obj.set("verified_bibliography", cur_bib)
    state_obj.update("nodes", {"librarian": {"count": len(verified)}})
    return verified
