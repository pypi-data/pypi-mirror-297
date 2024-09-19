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


class CartPaymentCheck(object):
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
        'check_number': 'int'
    }

    attribute_map = {
        'check_number': 'check_number'
    }

    def __init__(self, check_number=None):  # noqa: E501
        """CartPaymentCheck - a model defined in Swagger"""  # noqa: E501

        self._check_number = None
        self.discriminator = None

        if check_number is not None:
            self.check_number = check_number

    @property
    def check_number(self):
        """Gets the check_number of this CartPaymentCheck.  # noqa: E501

        Check number they are paying with  # noqa: E501

        :return: The check_number of this CartPaymentCheck.  # noqa: E501
        :rtype: int
        """
        return self._check_number

    @check_number.setter
    def check_number(self, check_number):
        """Sets the check_number of this CartPaymentCheck.

        Check number they are paying with  # noqa: E501

        :param check_number: The check_number of this CartPaymentCheck.  # noqa: E501
        :type: int
        """

        self._check_number = check_number

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
        if issubclass(CartPaymentCheck, dict):
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
        if not isinstance(other, CartPaymentCheck):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
