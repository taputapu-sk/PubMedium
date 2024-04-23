from xml.etree.ElementTree import Element as XElement
import xml.etree.ElementTree as ET

class PubMedAuthor:
    """
    Abstraction of a publication author.
    Heavily based upon the PubMed model.
    """

    def __init__(self):
        """
        Default constructor.
        Initializes all fields with default values.
        """
        self.id: int = 0            # Author ID private and unique to this system, since no other universally accepted
                                    # exists, and many authors have none (int).
        self.last_name: str = ""    # The family name of the author; str.
        self.fore_name: str = ""    # The given name of the author; str.
        self.initials: str = ""     # The initials of the author; str, optional.
        self.identification = {}    # A dictionary containing the author's identification IDs in one or more systems:
                                    # Key: PersonIdType; Value: the Id in that system.
        self.affiliations = []      # List of affiliation strings of the author; list[str], optional.

    def to_xml(self):
        x = XElement("PubMedAuthor")

        x.attrib['id'] = str(self.id)
        x.attrib['last_name'] = self.last_name
        x.attrib['fore_name'] = self.fore_name
        x.attrib['initials'] = self.initials

        x_identifications = ET.SubElement(x, 'identifications')
        for key in self.identification:
            x_identification = ET.SubElement(x_identifications, 'identification')
            x_identification.attrib['key'] = key
            x_identification.attrib['identification'] = self.identification[key]

        x_affiliations = ET.SubElement(x, 'affiliations')

        for affiliation in self.affiliations:
            x_affiliation = ET.SubElement(x_affiliations, 'affiliation')
            x_affiliation.text = affiliation

        return x

    def to_string(self, format: str = "lf") -> str:
        """
        String representation.
        :param format: Defines the format:
                       "fl": First Name, Last Name
                       "lf" (and default): Last Name, First Name.
        :return:
        """
        if format == "fl":
            if len(self.fore_name) > 0:
                return f"{self.fore_name} {self.last_name}"
            else:
                return self.last_name
        else:
            if len(self.fore_name) > 0:
                return f"{self.last_name}, {self.fore_name}"
            else:
                return self.last_name

    def __str__(self):
        """
        Default string representation.
        :return:
        """
        return self.to_string("lf")

