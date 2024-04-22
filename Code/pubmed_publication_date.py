from typing import Union
from xml.etree.ElementTree import Element as XElement
import xml.etree.ElementTree as ET

# Shortcut English month dictionary
_MONTH_DICTIONARY_EN = \
    {
        'JAN': 1,
        'FEB': 2,
        'MAR': 3,
        'APR': 4,
        'MAY': 5,
        'JUN': 6,
        'JUL': 7,
        'AUG': 8,
        'SEP': 9,
        'OCT': 10,
        'NOV': 11,
        'DEC': 12
    }

class PubMedPublicationDate:
    """
    Abstraction of a publication date.
    All components are integer; no validation is carried out.
    """
    def __init__(self, year: int = 0, month: Union[int, str] = 0, day: int = 0):
        """
        Creates an instance of PublicationDate.
        :param year: The year of publication
        :param month: The month of publication, either the number (1..12) or a string (case-insensitive).
                      If the input is a string, only the first three characters are taken into consideration.
                      No validation is carried out: if the string is not recognizable, the value of month will be 0 (invalid).
        :param day:
        """
        self.year = year

        if type(month) is int:
            self.month = month
        else:
            month_string = month.upper()[:3]
            if month_string in _MONTH_DICTIONARY_EN.keys():
                self.month = _MONTH_DICTIONARY_EN[month_string]
            else:
                self.month = 0

        self.day = day

    def __repr__(self):
        """
        String representation.
        :return:
        """
        if self.year <= 0:
            return ""

        if self.month > 0:
            if self.day > 0:
                return f"{self.year}-{self.month:02d}-{self.day:02d}"
            else:
                return f"{self.year}-{self.month:02d}"
        else:
            return f"{self.year}"

    def to_xml(self) -> XElement:
        x = XElement("PublicationDate")
        x.attrib['year'] = str(self.year)
        x.attrib['month'] = str(self.month)
        x.attrib['day'] = str(self.day)

        return x
