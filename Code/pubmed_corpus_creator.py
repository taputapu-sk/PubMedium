import os.path
import shutil
import subprocess

import requests
from bs4 import BeautifulSoup
from numpy.random import shuffle

from pubmed_fetcher import PubMedFetcher

# Base URL to fetch PDFs from:
NCBI_BASE_URL = "https://www.ncbi.nlm.nih.gov"

# Base URL to get PMC article pages:
PMC_BASE_ARTICLES_URL = "https://www.ncbi.nlm.nih.gov/pmc/articles/"

# Headers for HTTP request necessary for the PMC server to accept your request
# (without it, it would think that you are a bot, and refuse to response).
HEADERS_PDF_LINK = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
}

# Headers for HTTP request to download a PDF file.
HEADERS_PDF = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "application/pdf",
}

# Name for the temporary PDF file (presumed you are on Windows and C:\Temp exists).
TEMP_PDF = r"C:\Temp\temp_pubmed.pdf"
TEMP_TXT = r"C:\Temp\temp_pubmed.txt"


class PubMedCorpusCreator(PubMedFetcher):
    """
    Creator of topic text corpora from PubMed publications.
    """
    def create_corpus(self, size: int, topics: list[str], output_folder: str, corpus_name: str = ""):
        """
        Creates a text file corpus for a list of topics.
        :param size: The maximum size of the corpus to create.
        :param topics: List of topics to create the corpus from (combined by AND).
        :param output_folder: The name of the folder in which to create the corpus.
                              If the folder does not exist, it will be created.
        :param corpus_name: The name of the subfolder of output_folder in which to write the text files.
                            If left empty, the corpus name will be created using the topics.
        """
        if len(topics) == 0:
            print("No topics defined. Canceling.")
            return

        PubMedFetcher.print_intermediate_results = False
        ids = self._extract_ids_by_topics(topics)
        shuffle(ids)


        print(f"Found {len(ids)} publications for the topics.")
        publications = self._extract_publications(ids)

        if len(corpus_name) < 2:
            corpus_name = "_".join(topics)

        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        corpus_folder = f"{output_folder}/{corpus_name}"

        if not os.path.exists(corpus_folder):
            os.mkdir(corpus_folder)

        count = 0
        for publication in publications:
            if "PMC" in publication.article_ids:
                pmc_id = publication.article_ids["PMC"]
                pmc_url = self._get_pmc_url(pmc_id)
                pdf_link = self._get_pdf_link(pmc_url)

                if not self._download_pdf(pdf_link):
                    print("PDF link not found. Skipping.")
                    continue

                if not self._convert_to_text():
                    print("Conversion from PDF to text failed. Skipping.")
                    continue

                file_name = f"{corpus_folder}/{pmc_id}.txt"
                shutil.copyfile(TEMP_TXT, file_name)

                count += 1
                print(f"Copied {file_name} ({count} of {len(publications)})")

                if count >= size:
                    print(f"*** All publications processed. Created {count} text files.")
                    break

    # region Protected auxiliary
    def _get_pmc_url(self, pmc_id: str) -> str:
        """
        Gets the PMC URL from a PMC ID.
        :param pmc_id: The PMC ID.
        :return: The corresponding URL of the article.
        """
        return f"{PMC_BASE_ARTICLES_URL}{pmc_id}/"

    def _get_pdf_link(self, pmc_url: str) -> str:
        """
        Gets the link (URL) of the PDF file from a PMC ID.
        :param pmc_url: The PMC ID.
        :return: The URL of the PDF article.
        """
        request = requests.get(pmc_url, allow_redirects=True, headers=HEADERS_PDF_LINK)
        response = request.text

        soup = BeautifulSoup(response, "html.parser")

        x_link = soup.find("a", {"class": "int-view"})
        link = x_link.attrs["href"]
        return f"{NCBI_BASE_URL}{link}"

    def _download_pdf(self, pdf_link: str) -> bool:
        """
        Downloads the PDF article.
        :param pdf_link: The URL of the PDF file.
        :return: True, if the download succeeded.
        """
        response = requests.get(pdf_link, headers=HEADERS_PDF)

        try:
            # Write the downloaded PDF content to a file
            with open(TEMP_PDF, "wb") as file:
                file.write(response.content)

            return True
        except:
            return False

    def _convert_to_text(self) -> bool:
        """
        Converts the article from PDF format to plain text.
        :return: True if conversion succeeded.
        """
        try:
            # Added stderr=subprocess.DEVNULL to supress annoying warnings from MikTeX (ChatGPT).
            # no options used for pdftotext (except for -q). TODO: make the options as parameters.
            subprocess.run(["pdftotext", "-q", TEMP_PDF], stderr=subprocess.DEVNULL)
            return True
        except:
            return False
    # endregion

if __name__ == '__main__':
    fetcher = PubMedCorpusCreator()

    fetcher.create_corpus(5, ["dicom", "mri"], "C:/Temp")
