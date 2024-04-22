from xml.etree.ElementTree import Element as XElement
import xml.etree.ElementTree as ET

class PubMedReference:
    """
    Abstraction of a reference info for a publication.
    """
    def __init__(self):
        """
         Default constructor.
        Initializes all fields with default values.
        """
        self.citation: str = ""     # Citation string, str. Example: "Indian J Radiol Imaging. 2012 Jan;22(1):4-13"
        self.article_ids = {}       # # dictionary of the pubmed_ids of the reference;
                                    # key: BibliographicDatabase, value: the id in that system.

    def to_xml(self):
        x = XElement("PubMedReference")

        x.attrib['citation'] = self.citation

        x_article_ids = ET.SubElement(x, "article_ids")

        for article_id in self.article_ids:
            x_article_id = ET.SubElement(x_article_ids, "article_id")
            x_article_id.attrib['key'] = article_id
            x_article_id.attrib['value'] = self.article_ids[article_id]

        return x
