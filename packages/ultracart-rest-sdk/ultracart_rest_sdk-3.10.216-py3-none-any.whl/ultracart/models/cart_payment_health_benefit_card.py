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


class CartPaymentHealthBenefitCard(object):
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
        'health_benefit_card_expiration_month': 'int',
        'health_benefit_card_expiration_year': 'int',
        'health_benefit_card_number': 'str',
        'health_benefit_card_number_token': 'str',
        'health_benefit_card_verification_number': 'str',
        'health_benefit_card_verification_number_token': 'str'
    }

    attribute_map = {
        'health_benefit_card_expiration_month': 'health_benefit_card_expiration_month',
        'health_benefit_card_expiration_year': 'health_benefit_card_expiration_year',
        'health_benefit_card_number': 'health_benefit_card_number',
        'health_benefit_card_number_token': 'health_benefit_card_number_token',
        'health_benefit_card_verification_number': 'health_benefit_card_verification_number',
        'health_benefit_card_verification_number_token': 'health_benefit_card_verification_number_token'
    }

    def __init__(self, health_benefit_card_expiration_month=None, health_benefit_card_expiration_year=None, health_benefit_card_number=None, health_benefit_card_number_token=None, health_benefit_card_verification_number=None, health_benefit_card_verification_number_token=None):  # noqa: E501
        """CartPaymentHealthBenefitCard - a model defined in Swagger"""  # noqa: E501

        self._health_benefit_card_expiration_month = None
        self._health_benefit_card_expiration_year = None
        self._health_benefit_card_number = None
        self._health_benefit_card_number_token = None
        self._health_benefit_card_verification_number = None
        self._health_benefit_card_verification_number_token = None
        self.discriminator = None

        if health_benefit_card_expiration_month is not None:
            self.health_benefit_card_expiration_month = health_benefit_card_expiration_month
        if health_benefit_card_expiration_year is not None:
            self.health_benefit_card_expiration_year = health_benefit_card_expiration_year
        if health_benefit_card_number is not None:
            self.health_benefit_card_number = health_benefit_card_number
        if health_benefit_card_number_token is not None:
            self.health_benefit_card_number_token = health_benefit_card_number_token
        if health_benefit_card_verification_number is not None:
            self.health_benefit_card_verification_number = health_benefit_card_verification_number
        if health_benefit_card_verification_number_token is not None:
            self.health_benefit_card_verification_number_token = health_benefit_card_verification_number_token

    @property
    def health_benefit_card_expiration_month(self):
        """Gets the health_benefit_card_expiration_month of this CartPaymentHealthBenefitCard.  # noqa: E501

        Health benefit expiration month (1-12)  # noqa: E501

        :return: The health_benefit_card_expiration_month of this CartPaymentHealthBenefitCard.  # noqa: E501
        :rtype: int
        """
        return self._health_benefit_card_expiration_month

    @health_benefit_card_expiration_month.setter
    def health_benefit_card_expiration_month(self, health_benefit_card_expiration_month):
        """Sets the health_benefit_card_expiration_month of this CartPaymentHealthBenefitCard.

        Health benefit expiration month (1-12)  # noqa: E501

        :param health_benefit_card_expiration_month: The health_benefit_card_expiration_month of this CartPaymentHealthBenefitCard.  # noqa: E501
        :type: int
        """

        self._health_benefit_card_expiration_month = health_benefit_card_expiration_month

    @property
    def health_benefit_card_expiration_year(self):
        """Gets the health_benefit_card_expiration_year of this CartPaymentHealthBenefitCard.  # noqa: E501

        Health benefit card expiration year (four digit year)  # noqa: E501

        :return: The health_benefit_card_expiration_year of this CartPaymentHealthBenefitCard.  # noqa: E501
        :rtype: int
        """
        return self._health_benefit_card_expiration_year

    @health_benefit_card_expiration_year.setter
    def health_benefit_card_expiration_year(self, health_benefit_card_expiration_year):
        """Sets the health_benefit_card_expiration_year of this CartPaymentHealthBenefitCard.

        Health benefit card expiration year (four digit year)  # noqa: E501

        :param health_benefit_card_expiration_year: The health_benefit_card_expiration_year of this CartPaymentHealthBenefitCard.  # noqa: E501
        :type: int
        """

        self._health_benefit_card_expiration_year = health_benefit_card_expiration_year

    @property
    def health_benefit_card_number(self):
        """Gets the health_benefit_card_number of this CartPaymentHealthBenefitCard.  # noqa: E501

        Health benefit card number (masked to the last 4)  # noqa: E501

        :return: The health_benefit_card_number of this CartPaymentHealthBenefitCard.  # noqa: E501
        :rtype: str
        """
        return self._health_benefit_card_number

    @health_benefit_card_number.setter
    def health_benefit_card_number(self, health_benefit_card_number):
        """Sets the health_benefit_card_number of this CartPaymentHealthBenefitCard.

        Health benefit card number (masked to the last 4)  # noqa: E501

        :param health_benefit_card_number: The health_benefit_card_number of this CartPaymentHealthBenefitCard.  # noqa: E501
        :type: str
        """

        self._health_benefit_card_number = health_benefit_card_number

    @property
    def health_benefit_card_number_token(self):
        """Gets the health_benefit_card_number_token of this CartPaymentHealthBenefitCard.  # noqa: E501

        Hosted field token for the card number  # noqa: E501

        :return: The health_benefit_card_number_token of this CartPaymentHealthBenefitCard.  # noqa: E501
        :rtype: str
        """
        return self._health_benefit_card_number_token

    @health_benefit_card_number_token.setter
    def health_benefit_card_number_token(self, health_benefit_card_number_token):
        """Sets the health_benefit_card_number_token of this CartPaymentHealthBenefitCard.

        Hosted field token for the card number  # noqa: E501

        :param health_benefit_card_number_token: The health_benefit_card_number_token of this CartPaymentHealthBenefitCard.  # noqa: E501
        :type: str
        """

        self._health_benefit_card_number_token = health_benefit_card_number_token

    @property
    def health_benefit_card_verification_number(self):
        """Gets the health_benefit_card_verification_number of this CartPaymentHealthBenefitCard.  # noqa: E501

        Health benefit card verification number (masked)  # noqa: E501

        :return: The health_benefit_card_verification_number of this CartPaymentHealthBenefitCard.  # noqa: E501
        :rtype: str
        """
        return self._health_benefit_card_verification_number

    @health_benefit_card_verification_number.setter
    def health_benefit_card_verification_number(self, health_benefit_card_verification_number):
        """Sets the health_benefit_card_verification_number of this CartPaymentHealthBenefitCard.

        Health benefit card verification number (masked)  # noqa: E501

        :param health_benefit_card_verification_number: The health_benefit_card_verification_number of this CartPaymentHealthBenefitCard.  # noqa: E501
        :type: str
        """

        self._health_benefit_card_verification_number = health_benefit_card_verification_number

    @property
    def health_benefit_card_verification_number_token(self):
        """Gets the health_benefit_card_verification_number_token of this CartPaymentHealthBenefitCard.  # noqa: E501

        Hosted field token for the health benefit card verification number  # noqa: E501

        :return: The health_benefit_card_verification_number_token of this CartPaymentHealthBenefitCard.  # noqa: E501
        :rtype: str
        """
        return self._health_benefit_card_verification_number_token

    @health_benefit_card_verification_number_token.setter
    def health_benefit_card_verification_number_token(self, health_benefit_card_verification_number_token):
        """Sets the health_benefit_card_verification_number_token of this CartPaymentHealthBenefitCard.

        Hosted field token for the health benefit card verification number  # noqa: E501

        :param health_benefit_card_verification_number_token: The health_benefit_card_verification_number_token of this CartPaymentHealthBenefitCard.  # noqa: E501
        :type: str
        """

        self._health_benefit_card_verification_number_token = health_benefit_card_verification_number_token

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
        if issubclass(CartPaymentHealthBenefitCard, dict):
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
        if not isinstance(other, CartPaymentHealthBenefitCard):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
