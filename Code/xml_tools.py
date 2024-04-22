import xml.etree.ElementTree as ET
from typing import Optional


class XValues:
    """
    Extends etree.Element getting element and attribute value methods.
    While etree will throw an exception if an element or an attribute is not found,
    XValues will instead return a default value.
    """

    # region String values
    @classmethod
    def element_string(cls, x: ET.Element, tag: str, default_value: str = None) -> str:
        element = XValues._get_element(x, tag)

        if element is None:
            if default_value is None:
                return str()
            else:
                return default_value
        else:
            return element.text

    @classmethod
    def attribute_string(cls, x: ET.Element, tag: str, default_value: str = None) -> str:
        attribute_value = XValues._get_attribute(x, tag)

        if attribute_value is None:
            if default_value is None:
                return str()
            else:
                return default_value
        else:
            return attribute_value

    # endregion

    # region Integer methods
    @classmethod
    def element_int(cls, x: ET.Element, tag: str, default_value: int = None) -> int:
        element = XValues._get_element(x, tag)

        if element is None:
            if default_value is None:
                return int()
            else:
                return default_value
        else:
            source = element.text
            try:
                return int(source)
            except ValueError:
                if default_value is None:
                    return int()
                else:
                    return default_value

    @classmethod
    def attribute_int(cls, x: ET.Element, tag: str, default_value: int = None) -> int:
        source = XValues._get_attribute(x, tag)

        if source is None:
            if default_value is None:
                return int()
            else:
                return default_value
        else:
            try:
                return int(source)
            except ValueError:
                if default_value is None:
                    return int()
                else:
                    return default_value
    # endregion

    # region Float methods
    @classmethod
    def element_float(cls, x: ET.Element, tag: str, default_value: float = None) -> float:
        element = XValues._get_element(x, tag)

        if element is None:
            if default_value is None:
                return float()
            else:
                return default_value
        else:
            source = element.text
            try:
                return float(source)
            except ValueError:
                if default_value is None:
                    return float()
                else:
                    return default_value

    @classmethod
    def attribute_float(cls, x: ET.Element, tag: str, default_value: float = None) -> float:
        source = XValues._get_attribute(x, tag)

        if source is None:
            if default_value is None:
                return float()
            else:
                return default_value
        else:
            try:
                return float(source)
            except ValueError:
                if default_value is None:
                    return float()
                else:
                    return default_value
    # endregion

    # region Boolean methods
    @classmethod
    def element_bool(cls, x: ET.Element, tag: str, default_value: bool = None) -> bool:
        element = XValues._get_element(x, tag)

        if element is None:
            if default_value is None:
                return bool()
            else:
                return default_value
        else:
            source = element.text
            try:
                return bool(source)
            except ValueError:
                if default_value is None:
                    return bool()
                else:
                    return default_value

    @classmethod
    def attribute_bool(cls, x: ET.Element, tag: str, default_value: bool = None) -> bool:
        source = XValues._get_attribute(x, tag)

        if source is None:
            if default_value is None:
                return bool()
            else:
                return default_value
        else:
            try:
                return bool(source)
            except ValueError:
                if default_value is None:
                    return bool()
                else:
                    return default_value
    # endregion

    # region Protected Auxiliary
    @classmethod
    def _get_element(cls, x: ET.Element, tag: str) -> Optional[ET.Element]:
        """
        Tries to get an element with a given tag name of an etree element.
        :param x: The element to find the element in.
        :param tag: The name of the element to look for.
        :return: The element, if found, otherwise None.
        """
        element = x.find(tag)

        if element is None:
            return None
        else:
            return element

    @classmethod
    def _get_attribute(cls, x: ET.Element, tag: str) -> Optional[str]:
        """
        Tries to get an attribute with a given tag name of an etree element.
        :param x: The element to find the attribute in.
        :param tag: The name of the attribute to look for.
        :return: The string value of the attribute, if found, otherwise None.
        """

        return x.attrib[tag]
    # endregion
