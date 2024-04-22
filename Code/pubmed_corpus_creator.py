import os.path
import shutil
import subprocess

import requests
from pathlib import Path
from Code.pubmed_fetcher import PubMedFetcher
from numpy.random import shuffle
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

NCBI_BASE_URL = "https://www.ncbi.nlm.nih.gov"
PMC_BASE_ARTICLES_URL = "https://www.ncbi.nlm.nih.gov/pmc/articles/"
HEADERS_PDF_LINK = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}

HEADERS_PDF = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "application/pdf",
}

TEMP_PDF = r"C:\Temp\temp_pubmed.pdf"
TEMP_TXT = r"C:\Temp\temp_pubmed.txt"


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

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        corpus_folder = f"{output_folder}/{corpus_name}"

        if not os.path.exists(corpus_folder):
            os.mkdir(corpus_folder)

        for publication in publications:
            if "PMC" in publication.article_ids:
                pmc_id = publication.article_ids["PMC"]
                pmc_url = self._get_pmc_url(pmc_id)
                pdf_link = self._get_pdf_link(pmc_url)

                if not self._download_pdf(pdf_link):
                    continue

                if not self._convert_to_text():
                    continue

                file_name = f"{corpus_folder}/{pmc_id}.txt"
                shutil.copyfile(TEMP_TXT, file_name)

                print(f"Copied {file_name}")


    def _get_pmc_url(self, pmc_id: str) -> str:
        return f"{PMC_BASE_ARTICLES_URL}{pmc_id}/"

    def _get_pdf_link(self, pmc_url: str) -> str:
        request = requests.get(pmc_url, allow_redirects=True, headers=HEADERS_PDF_LINK)
        response = request.text

        soup = BeautifulSoup(response, parser="html")

        x_link = soup.find("a", {"class": "int-view"})
        link = x_link.attrs["href"]
        return f"{NCBI_BASE_URL}{link}"

    def _download_pdf(self, pdf_link: str) -> bool:
        # Send request to download the PDF
        response = requests.get(pdf_link, headers=HEADERS_PDF)

        try:
            # Write the downloaded PDF content to a file
            with open(TEMP_PDF, "wb") as file:
                file.write(response.content)

            return True
        except:
            return False

    def _convert_to_text(self) -> bool:
        try:
            #subprocess.run(["pdftotext", "-layout", "-nodiag", TEMP_PDF])
            subprocess.run(["pdftotext", TEMP_PDF])
            return True
        except:
            return False

if __name__ == '__main__':
    fetcher = PubMedCorpusCreator()

    fetcher.create_corpus(100, ["dicom", "mri", "prostate"], "C:/Temp", "dicom_mri")
