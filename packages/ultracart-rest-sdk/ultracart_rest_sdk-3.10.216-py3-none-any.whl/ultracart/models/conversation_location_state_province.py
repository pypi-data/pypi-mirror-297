# coding: utf-8

"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ConversationLocationStateProvince(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'abbreviation': 'str',
        'name': 'str'
    }

    attribute_map = {
        'abbreviation': 'abbreviation',
        'name': 'name'
    }

    def __init__(self, abbreviation=None, name=None):  # noqa: E501
        """ConversationLocationStateProvince - a model defined in Swagger"""  # noqa: E501

        self._abbreviation = None
        self._name = None
        self.discriminator = None

        if abbreviation is not None:
            self.abbreviation = abbreviation
        if name is not None:
            self.name = name

    @property
    def abbreviation(self):
        """Gets the abbreviation of this ConversationLocationStateProvince.  # noqa: E501


        :return: The abbreviation of this ConversationLocationStateProvince.  # noqa: E501
        :rtype: str
        """
        return self._abbreviation

    @abbreviation.setter
    def abbreviation(self, abbreviation):
        """Sets the abbreviation of this ConversationLocationStateProvince.


        :param abbreviation: The abbreviation of this ConversationLocationStateProvince.  # noqa: E501
        :type: str
        """

        self._abbreviation = abbreviation

    @property
    def name(self):
        """Gets the name of this ConversationLocationStateProvince.  # noqa: E501


        :return: The name of this ConversationLocationStateProvince.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ConversationLocationStateProvince.


        :param name: The name of this ConversationLocationStateProvince.  # noqa: E501
        :type: str
        """

        self._name = name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(ConversationLocationStateProvince, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ConversationLocationStateProvince):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
