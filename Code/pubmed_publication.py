from dataclasses import dataclass
from pubmed_author import PubMedAuthor
from pubmed_publication_date import PubMedPublicationDate
from pubmed_reference import PubMedReference
from xml.etree.ElementTree import Element as XElement
import xml.etree.ElementTree as ET

@dataclass
class PubMedPublication:
    """
    Describes a PubMed publication.
    """
    publication_id: int = 0
    ISSN: str = ""                              # The ISSN of the publication series.
    volume: str = ""                            # The volume; string.
    issue: str = ""                             # The number (issue) of the publication.
    pagination: str = ""                        # The pagination string.
    journal_title: str = ""                     # The full name of the journal, e.g. "Abstracts of radiology".
    journal_title_abbreviation: str = ""        # Journal title abbreviation, e.g. "Int J Comput Assist Radiol Surg".
    article_title: str = ""                     # The title of the article.
    abstract: str = ""                          # The abstract.
    language: str = ""                          # Language code in ISO 639 Alpha3.


    def __init__(self):
        """
        Mutable defaults such as lists are not supported in dataclass model,
        therefore must be declared in constructor.
        """
        self.article_ids: dict[str, str] = {}                                  # Dictionary of the IDs of the article:
                                                                                # key: PublicationIdType;
                                                                                # Value: the Id in that system,
                                                                                # e.g. "doi": "2345.4567.234".
        self.keywords: list[str] = []                                           # List of keywords.
        self.publication_date: PubMedPublicationDate = PubMedPublicationDate()  # Date of publication.
        self.authors: list[PubMedAuthor] = []                                   # List of the authors.
        self.references: list[PubMedReference] = []                             # List of references.

    def to_xml(self) -> XElement:
        x = XElement("PubMedPublication")
        x.attrib['id'] = str(self.publication_id)
        x.attrib['ISSN'] = self.ISSN
        x.attrib['volume'] = self.volume
        x.attrib['issue'] = self.issue
        x.attrib['pagination'] = self.pagination
        x.attrib['language'] = self.language

        x_journal_title = ET.SubElement(x, 'journal_title')
        x_journal_title.text = self.journal_title
        x_journal_title_abbreviation = ET.SubElement(x, 'journal_title_abbreviation')
        x_journal_title_abbreviation.text = self.journal_title_abbreviation

        x_article_title = ET.SubElement(x, 'article_title')
        x_article_title.text = self.article_title

        x_abstract = ET.SubElement(x, 'abstract')
        x_abstract.text = self.abstract

        x_article_ids = ET.SubElement(x, 'article_ids')
        for article_id in self.article_ids:
            x_article_id = ET.SubElement(x_article_ids, "article_id")
            x_article_id.text = article_id

        x_keywords = ET.SubElement(x, 'keywords')
        for keyword in self.keywords:
            x_keyword = ET.SubElement(x_keywords, "keyword")
            x_keyword.text = keyword

        x.append(self.publication_date.to_xml())

        x_authors = ET.SubElement(x, 'authors')

        for author in self.authors:
            x_authors.append(author.to_xml())

        x_references = ET.SubElement(x, "references")

        for reference in self.references:
            x_references.append(reference.to_xml())

        return x

    def to_bibtex_entry(self) -> str:
        # @article{PMID:271968,
        # author = "Sanger, F. and Nicklen, S. and Coulson, A. R.",
        # doi = "10.1073/pnas.74.12.5463",
        # url = "https://doi.org/10.1073/pnas.74.12.5463",
        # year = "1977",
        # publisher = "Proceedings of the National Academy of Sciences",
        # volume = "74",
        # number = "12",
        # pages = "5463--5467",
        # title = "{DNA} sequencing with chain-terminating inhibitors",
        # journal = "Proceedings of the National Academy of Sciences",
        # PMID = "271968"
        # }
        result = f"@article{{PMID:{self.publication_id},\n"
        if len(self.authors) == 0:
            authors = "n.a."
        elif len(self.authors) <= 3:
            authors = [str(author) for author in self.authors]
            authors = " and ".join(authors)
        else:
            authors = f"{str(self.authors[0])} et al."

        result += f"\tauthor = \"{authors}\",\n"

        doi = self.article_ids["DOI"] if "DOI" in self.article_ids else ""
        result += f"\tdoi = \"{doi}\",\n"
        result += f"\tyear = \"{self.publication_date.year}\",\n"
        result += f"\tvolume = \"{self.volume}\",\n"
        result += f"\tnumber = \"{self.issue}\",\n"
        result += f"\tpages = \"{self.pagination}\",\n"
        result += f"\ttitle = \"{self.article_title}\",\n"
        result += f"\tjournal = \"{self.journal_title}\"\n"
        result += "}"

        return result

if __name__ == '__main__':
    pmp = PubMedPublication()



