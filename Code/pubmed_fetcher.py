from typing import Optional

import requests
import xml.etree.ElementTree as ET

from pubmed_publication import PubMedPublication
from pubmed_author import PubMedAuthor
from pubmed_reference import PubMedReference

import xml_tools

# region Constants
NCBI_SEARCH_REQUEST_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed"   # default URL base to query for publication IDs.
NCBI_FETCH_REQUEST_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed"     # default URL base to fetch the publication infos.
NUMBER_OF_IDS_IN_PARTIAL_REQUEST = 1000                                                             # Number of IDs in a partial request for IDs.
DEFAULT_SIZE_OF_EXTRACTION_PORTION = 200                                                            # Default number of entries in an extraction portion.
# endregion

class PubMedFetcher:
    # region Class variables
    print_intermediate_results = True           # If set to True (default), all intermediate results will be printed.
    extract_references = True                   # If set to True (default, references will be extracted):
    # endregion

    # region Public features
    def fetch_by_topics(self, topics: list[str], from_year: int = 1800) -> list[PubMedPublication]:
        """
        Fetches publications by topic list. At the moment, only the 'AND' combination of topics is supported.
        TODO: support the 'OR' combination of topics.
        :param topics: List of topics.
        :param from_year: Minimum year from which to start. Default: 1800, that is, hopefully, all stuff.
        :return: List of publications found.
        """
        ids = self._extract_ids_by_topics(topics)

        return self._extract_publications_by_id_list(ids)
    # endregion

    # region Protected Auxiliary
    def _extract_ids_by_topics(self, topics: list[str]) -> list[int]:
        """
        Retrieves PubMed IDs for a list of search topics.
        :param topics: A list of topics to find IDs for.
        :return: List of PubMed IDs found.
        """
        result = []
        total_number_of_ids = self._get_count_of_topic_findings(topics)

        if total_number_of_ids <= 0:
            return result

        count_ids_downloaded = 0
        start_index = 0

        while count_ids_downloaded < total_number_of_ids:
            ids_portion = self._download_portion_of_topic_ids \
                    (
                        topics,
                        start_index,
                        NUMBER_OF_IDS_IN_PARTIAL_REQUEST
                    )
            if PubMedFetcher.print_intermediate_results:
                print(f"Extracted {len(ids_portion)} topic IDs out of {total_number_of_ids}")

            result += ids_portion
            count_ids_downloaded += len(ids_portion)
            start_index = len(result)

        return result

    def _get_count_of_topic_findings(self, topics: list[str]) -> int:
        """
        Gets the count of findings for a list of search topics.
        :param topics: The search topics.
        :return: The number of IDs corresponding to the pattern.
        """
        request_url = f"{NCBI_SEARCH_REQUEST_BASE}&rettype=count&term={'+'.join(topics)}"

        # TODO: can be changed?
        try:
            request = requests.request("get", request_url)
            response = request.text
            tree = ET.fromstring(response)
            x_count = tree.find('Count')
            return int(x_count.text)
        except:
            return 0

    def _download_portion_of_topic_ids(self, topics: list[str], start_index: int, number_of_entries: int) -> list[str]:
        """
        Downloads a portion of size number_of_entries from a PubMed IDs from an ID list, starting from the index start_index.
        The REST API does not allow to download all IDs at once, but is rather limited to a maximum number od IDs per step (100000).
        :param topics: The list of search topics.
        :param start_index: The index to start from.
        :param number_of_entries: The number of indices to download.
        :return: The list of Pubmed IDs for the portion.
        """
        result = list[str]()
        search_url = f"{NCBI_SEARCH_REQUEST_BASE}&retmax={number_of_entries}&retstart={start_index}&term={'+'.join(topics)}"
        request = requests.request("get", search_url)
        response = request.text
        tree = ET.fromstring(response)
        x_id_list = tree.find('IdList')
        for xId in x_id_list.findall('Id'):
            result.append(xId.text)

        return result

    def _extract_publications(self, pubmed_ids: list[int]) -> list[PubMedPublication]:
        """
        Extracts a number od publications by their PubMed IDs.
        :param pubmed_ids: List of PubMed IDs to extract.
        :return: Resulting list of successfully extracted publications.
        """
        result = []

        for start_index in range(0, len(pubmed_ids), DEFAULT_SIZE_OF_EXTRACTION_PORTION):
            ids_to_process = pubmed_ids[start_index: start_index + DEFAULT_SIZE_OF_EXTRACTION_PORTION]
            portion = self._extract_publications_by_id_list(ids_to_process)
            result += portion

        return result

    def _extract_publications_by_id_list(self, pubmed_ids: list[int]) -> list[PubMedPublication]:
        """
        Extracts a number of publications for a list of PubMed IDs.
        :param pubmed_ids: The list of PubMed IDs to extract.
        :return: The resulting list of publications extracted.
        """
        result = []

        id_strings = [str(id) for id in pubmed_ids]
        fetch_url = f"{NCBI_FETCH_REQUEST_BASE}&retmode=xml&id={','.join(id_strings)}"

        request = requests.request("get", fetch_url)

        if request.status_code == 414:
            raise ValueError("STATUS_URI_TOO_LONG")

        response = request.text

        tree = ET.fromstring(response)

        count = 1
        for x_pubmed_article in tree.findall('PubmedArticle'):
            publication = self._extract_publication(x_pubmed_article)

            if publication is not None:
                result.append(publication)

                if PubMedFetcher.print_intermediate_results:
                    print(f"Extracted {count} publications out of {len(pubmed_ids)}")
                    count += 1

        return result

    def _extract_publication(self, x_pubmed_article: ET.Element) -> Optional[PubMedPublication]:
        """
        Extracts a publication using an xml.etree.ElementTree.Element as the input.
        :param x_pubmed_article: The instance of xml.etree.ElementTree.Element to extract from.
        :return: Resulting instance of Publication, if succeeded, otherwise None.
        """
        publication = PubMedPublication()
        x_medline_citation = x_pubmed_article.find('MedlineCitation')

        # extract PMID
        publication.publication_id = xml_tools.XValues.element_int(x_medline_citation, "PMID")

        if publication.publication_id <= 0:     # extraction of PMID did not work; return invalid publication
            return publication

        x_article = x_medline_citation.find("Article")
        x_journal = x_article.find("Journal")

        # extract ISSN
        publication.ISSN = xml_tools.XValues.element_string(x_journal, "ISSN")

        # extract volume, issue, and publication date
        x_journal_issue = x_journal.find("JournalIssue")
        publication.volume = xml_tools.XValues.element_string(x_journal_issue, "Volume")
        publication.issue = xml_tools.XValues.element_string(x_journal_issue, "Issue")

        x_pubdate = x_journal_issue.find("PubDate")
        publication.publication_date.year = xml_tools.XValues.element_int(x_pubdate, "Year")
        publication.publication_date.month = xml_tools.XValues.element_int(x_pubdate, "Month")
        publication.publication_date.day = xml_tools.XValues.element_int(x_pubdate, "Day")

        publication.journal_title = xml_tools.XValues.element_string(x_journal, "Title")
        publication.journal_title_abbreviation = xml_tools.XValues.element_string(x_journal, "ISOAbbreviation")

        # extract title
        publication.article_title = xml_tools.XValues.element_string(x_article, "ArticleTitle")

        # extract pagination
        x_pagination = x_article.find("Pagination")

        if x_pagination is not None:
            publication.pagination = xml_tools.XValues.element_string(x_pagination, "MedlinePgn")

        # extract abstract
        x_abstract = x_article.find("Abstract")

        if x_abstract is not None:
            for x_abstract_text in x_abstract.findall("AbstractText"):
                publication.abstract += f"{x_abstract_text.text}\n"

        # extract authors
        x_authors = x_article.find("AuthorList")
        if x_authors is not None:
            for x_author in x_authors.findall("Author"):
                author = PubMedAuthor()
                # TODO: assign local author ID
                #  author.id = ...
                author.last_name = xml_tools.XValues.element_string(x_author, "LastName")
                author.fore_name = xml_tools.XValues.element_string(x_author, "ForeName")
                author.initials = xml_tools.XValues.element_string(x_author, "Initials")

                for x_author_identifier in x_author.findall("Identifier"):
                    source = xml_tools.XValues.attribute_string(x_author_identifier, "Source")
                    identifier = x_author_identifier.text
                    author.identification[source] = identifier

                for x_affiliation_info in x_author.findall("AffiliationInfo"):
                    affiliation = xml_tools.XValues.element_string(x_affiliation_info, "Affiliation")
                    if affiliation is not None and len(affiliation) > 0:
                        author.affiliations.append(affiliation)

                publication.authors.append(author)

        # extract language
        publication.language = xml_tools.XValues.element_string(x_article, "Language")

        # extract keywords
        x_keywords = x_medline_citation.find("KeywordList")
        if x_keywords is not None:
            for x_keyword in x_keywords.findall("Keyword"):
                publication.keywords.append(x_keyword.text)

        # extract references
        if PubMedFetcher.extract_references:
            x_pubmed_data = x_pubmed_article.find("PubmedData")

            # extract article IDs (DOI, PMC, etc.)
            x_articel_id_list = x_pubmed_data.find("ArticleIdList")
            for x_article_id in x_articel_id_list.findall("ArticleId"):
                publication_id_type = xml_tools.XValues.attribute_string(x_article_id, "IdType").upper()
                publication.article_ids[publication_id_type] = x_article_id.text

            x_references = x_pubmed_data.find("ReferenceList")
            if x_references is not None:
                for x_reference in x_references.findall("Reference"):
                    reference = PubMedReference()
                    reference.citation = xml_tools.XValues.element_string(x_reference, "Citation")

                    x_reference_ids = x_reference.find("ArticleIdList")

                    if x_reference_ids is not None:
                        for x_reference_id in x_reference_ids.findall("ArticleId"):
                            id_type = xml_tools.XValues.attribute_string(x_reference_id, "IdType").upper()
                            reference.article_ids[id_type] = x_reference_id.text

                    publication.references.append(reference)

        return publication
    # endregion


if __name__ == '__main__':
    topics = ['dicom', 'prostate', 'mri']

    fetcher = PubMedFetcher()
    PubMedFetcher.extract_references = False

    publications = fetcher.fetch_by_topics(topics)

    for publication in publications:
        print(publication)
