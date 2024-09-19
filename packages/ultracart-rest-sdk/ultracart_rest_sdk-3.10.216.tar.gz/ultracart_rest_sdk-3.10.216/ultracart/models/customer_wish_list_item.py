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


class CustomerWishListItem(object):
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
        'add_dts': 'str',
        'comments': 'str',
        'customer_profile_oid': 'int',
        'customer_wishlist_item_oid': 'int',
        'merchant_item_oid': 'int',
        'position': 'int',
        'priority': 'int'
    }

    attribute_map = {
        'add_dts': 'add_dts',
        'comments': 'comments',
        'customer_profile_oid': 'customer_profile_oid',
        'customer_wishlist_item_oid': 'customer_wishlist_item_oid',
        'merchant_item_oid': 'merchant_item_oid',
        'position': 'position',
        'priority': 'priority'
    }

    def __init__(self, add_dts=None, comments=None, customer_profile_oid=None, customer_wishlist_item_oid=None, merchant_item_oid=None, position=None, priority=None):  # noqa: E501
        """CustomerWishListItem - a model defined in Swagger"""  # noqa: E501

        self._add_dts = None
        self._comments = None
        self._customer_profile_oid = None
        self._customer_wishlist_item_oid = None
        self._merchant_item_oid = None
        self._position = None
        self._priority = None
        self.discriminator = None

        if add_dts is not None:
            self.add_dts = add_dts
        if comments is not None:
            self.comments = comments
        if customer_profile_oid is not None:
            self.customer_profile_oid = customer_profile_oid
        if customer_wishlist_item_oid is not None:
            self.customer_wishlist_item_oid = customer_wishlist_item_oid
        if merchant_item_oid is not None:
            self.merchant_item_oid = merchant_item_oid
        if position is not None:
            self.position = position
        if priority is not None:
            self.priority = priority

    @property
    def add_dts(self):
        """Gets the add_dts of this CustomerWishListItem.  # noqa: E501

        Add date  # noqa: E501

        :return: The add_dts of this CustomerWishListItem.  # noqa: E501
        :rtype: str
        """
        return self._add_dts

    @add_dts.setter
    def add_dts(self, add_dts):
        """Sets the add_dts of this CustomerWishListItem.

        Add date  # noqa: E501

        :param add_dts: The add_dts of this CustomerWishListItem.  # noqa: E501
        :type: str
        """

        self._add_dts = add_dts

    @property
    def comments(self):
        """Gets the comments of this CustomerWishListItem.  # noqa: E501

        Comments  # noqa: E501

        :return: The comments of this CustomerWishListItem.  # noqa: E501
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """Sets the comments of this CustomerWishListItem.

        Comments  # noqa: E501

        :param comments: The comments of this CustomerWishListItem.  # noqa: E501
        :type: str
        """
        if comments is not None and len(comments) > 1024:
            raise ValueError("Invalid value for `comments`, length must be less than or equal to `1024`")  # noqa: E501

        self._comments = comments

    @property
    def customer_profile_oid(self):
        """Gets the customer_profile_oid of this CustomerWishListItem.  # noqa: E501

        Customer profile object identifier  # noqa: E501

        :return: The customer_profile_oid of this CustomerWishListItem.  # noqa: E501
        :rtype: int
        """
        return self._customer_profile_oid

    @customer_profile_oid.setter
    def customer_profile_oid(self, customer_profile_oid):
        """Sets the customer_profile_oid of this CustomerWishListItem.

        Customer profile object identifier  # noqa: E501

        :param customer_profile_oid: The customer_profile_oid of this CustomerWishListItem.  # noqa: E501
        :type: int
        """

        self._customer_profile_oid = customer_profile_oid

    @property
    def customer_wishlist_item_oid(self):
        """Gets the customer_wishlist_item_oid of this CustomerWishListItem.  # noqa: E501

        Customer wishlist item object identifier  # noqa: E501

        :return: The customer_wishlist_item_oid of this CustomerWishListItem.  # noqa: E501
        :rtype: int
        """
        return self._customer_wishlist_item_oid

    @customer_wishlist_item_oid.setter
    def customer_wishlist_item_oid(self, customer_wishlist_item_oid):
        """Sets the customer_wishlist_item_oid of this CustomerWishListItem.

        Customer wishlist item object identifier  # noqa: E501

        :param customer_wishlist_item_oid: The customer_wishlist_item_oid of this CustomerWishListItem.  # noqa: E501
        :type: int
        """

        self._customer_wishlist_item_oid = customer_wishlist_item_oid

    @property
    def merchant_item_oid(self):
        """Gets the merchant_item_oid of this CustomerWishListItem.  # noqa: E501

        Merchant item object identifier  # noqa: E501

        :return: The merchant_item_oid of this CustomerWishListItem.  # noqa: E501
        :rtype: int
        """
        return self._merchant_item_oid

    @merchant_item_oid.setter
    def merchant_item_oid(self, merchant_item_oid):
        """Sets the merchant_item_oid of this CustomerWishListItem.

        Merchant item object identifier  # noqa: E501

        :param merchant_item_oid: The merchant_item_oid of this CustomerWishListItem.  # noqa: E501
        :type: int
        """

        self._merchant_item_oid = merchant_item_oid

    @property
    def position(self):
        """Gets the position of this CustomerWishListItem.  # noqa: E501

        Position in wishlist  # noqa: E501

        :return: The position of this CustomerWishListItem.  # noqa: E501
        :rtype: int
        """
        return self._position

    @position.setter
    def position(self, position):
        """Sets the position of this CustomerWishListItem.

        Position in wishlist  # noqa: E501

        :param position: The position of this CustomerWishListItem.  # noqa: E501
        :type: int
        """

        self._position = position

    @property
    def priority(self):
        """Gets the priority of this CustomerWishListItem.  # noqa: E501

        Priority of wishlist item, 3 being low priority and 5 is high priority.  # noqa: E501

        :return: The priority of this CustomerWishListItem.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this CustomerWishListItem.

        Priority of wishlist item, 3 being low priority and 5 is high priority.  # noqa: E501

        :param priority: The priority of this CustomerWishListItem.  # noqa: E501
        :type: int
        """

        self._priority = priority

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
        if issubclass(CustomerWishListItem, dict):
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
        if not isinstance(other, CustomerWishListItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
