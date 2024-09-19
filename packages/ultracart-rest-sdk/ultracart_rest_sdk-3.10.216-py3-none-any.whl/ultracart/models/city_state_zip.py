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


class CityStateZip(object):
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
        'city': 'str',
        'error': 'str',
        'state': 'str',
        'valid_zip': 'bool',
        'zip': 'str'
    }

    attribute_map = {
        'city': 'city',
        'error': 'error',
        'state': 'state',
        'valid_zip': 'validZip',
        'zip': 'zip'
    }

    def __init__(self, city=None, error=None, state=None, valid_zip=None, zip=None):  # noqa: E501
        """CityStateZip - a model defined in Swagger"""  # noqa: E501

        self._city = None
        self._error = None
        self._state = None
        self._valid_zip = None
        self._zip = None
        self.discriminator = None

        if city is not None:
            self.city = city
        if error is not None:
            self.error = error
        if state is not None:
            self.state = state
        if valid_zip is not None:
            self.valid_zip = valid_zip
        if zip is not None:
            self.zip = zip

    @property
    def city(self):
        """Gets the city of this CityStateZip.  # noqa: E501


        :return: The city of this CityStateZip.  # noqa: E501
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city):
        """Sets the city of this CityStateZip.


        :param city: The city of this CityStateZip.  # noqa: E501
        :type: str
        """

        self._city = city

    @property
    def error(self):
        """Gets the error of this CityStateZip.  # noqa: E501


        :return: The error of this CityStateZip.  # noqa: E501
        :rtype: str
        """
        return self._error

    @error.setter
    def error(self, error):
        """Sets the error of this CityStateZip.


        :param error: The error of this CityStateZip.  # noqa: E501
        :type: str
        """

        self._error = error

    @property
    def state(self):
        """Gets the state of this CityStateZip.  # noqa: E501


        :return: The state of this CityStateZip.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this CityStateZip.


        :param state: The state of this CityStateZip.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def valid_zip(self):
        """Gets the valid_zip of this CityStateZip.  # noqa: E501


        :return: The valid_zip of this CityStateZip.  # noqa: E501
        :rtype: bool
        """
        return self._valid_zip

    @valid_zip.setter
    def valid_zip(self, valid_zip):
        """Sets the valid_zip of this CityStateZip.


        :param valid_zip: The valid_zip of this CityStateZip.  # noqa: E501
        :type: bool
        """

        self._valid_zip = valid_zip

    @property
    def zip(self):
        """Gets the zip of this CityStateZip.  # noqa: E501


        :return: The zip of this CityStateZip.  # noqa: E501
        :rtype: str
        """
        return self._zip

    @zip.setter
    def zip(self, zip):
        """Sets the zip of this CityStateZip.


        :param zip: The zip of this CityStateZip.  # noqa: E501
        :type: str
        """

        self._zip = zip

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
        if issubclass(CityStateZip, dict):
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
        if not isinstance(other, CityStateZip):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
