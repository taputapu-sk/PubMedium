import requests

from Code.pubmed_fetcher import PubMedFetcher
from numpy.random import shuffle
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

NCBI_BASE_URL = "https://www.ncbi.nlm.nih.gov"
PMC_BASE_ARTICLES_URL = "https://www.ncbi.nlm.nih.gov/pmc/articles/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    }

class PubMedCorpusCreator(PubMedFetcher):
    """
    Vehicula, suspendisse massa gravida. Turpis velit commodo lobortis tristique hendrerit, scelerisque nec iaculis.
    Vulputate pellentesque rutrum lorem mattis litora tempor. Lacus curae; posuere, habitasse interdum.
    Feugiat torquent etiam consequat ornare nunc gravida feugiat quam purus scelerisque bibendum.
    Sapien adipiscing turpis id auctor in ligula parturient. Nisl nam donec congue curae; fusce
    lacinia duis vitae.
    """
    def create_corpus(self, size: int, topics: list[str], output_folder: str, corpus_name: str):
        ids = self._extract_ids_by_topics(topics)
        shuffle(ids)

        publications = self._extract_publications(ids)

        for publication in publications:
            if "PMC" in publication.article_ids:
                pmc_url = self._get_pmc_url(publication.article_ids["PMC"])
                pdf_link = self._get_pdf_link(pmc_url)
                pass
                # print(publication.article_ids["PMC"])


    def _get_pmc_url(self, pmc_id: str) -> str:
        return f"{PMC_BASE_ARTICLES_URL}{pmc_id}/"

    def _get_pdf_link(self, pmc_url: str) -> str:
        request = requests.get(pmc_url, allow_redirects=True, headers=HEADERS)
        response = request.text

        soup = BeautifulSoup(response)

        x_link = soup.find("a", {"class": "int-view"})
        link = x_link.attrs["href"]
        return f"{NCBI_BASE_URL}{link}"

if __name__ == '__main__':
    fetcher = PubMedCorpusCreator()

    fetcher.create_corpus(100, ["dicom", "mri", "prostate"], "", "")
