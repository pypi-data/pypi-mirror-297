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


class CartCheckout(object):
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
        'comments': 'str',
        'current_step': 'str',
        'custom_field1': 'str',
        'custom_field10': 'str',
        'custom_field2': 'str',
        'custom_field3': 'str',
        'custom_field4': 'str',
        'custom_field5': 'str',
        'custom_field6': 'str',
        'custom_field7': 'str',
        'custom_field8': 'str',
        'custom_field9': 'str',
        'ip_address': 'str',
        'return_code': 'str',
        'return_url': 'str',
        'screen_branding_theme_code': 'str',
        'storefront_host_name': 'str',
        'user_agent': 'str'
    }

    attribute_map = {
        'comments': 'comments',
        'current_step': 'current_step',
        'custom_field1': 'custom_field1',
        'custom_field10': 'custom_field10',
        'custom_field2': 'custom_field2',
        'custom_field3': 'custom_field3',
        'custom_field4': 'custom_field4',
        'custom_field5': 'custom_field5',
        'custom_field6': 'custom_field6',
        'custom_field7': 'custom_field7',
        'custom_field8': 'custom_field8',
        'custom_field9': 'custom_field9',
        'ip_address': 'ip_address',
        'return_code': 'return_code',
        'return_url': 'return_url',
        'screen_branding_theme_code': 'screen_branding_theme_code',
        'storefront_host_name': 'storefront_host_name',
        'user_agent': 'user_agent'
    }

    def __init__(self, comments=None, current_step=None, custom_field1=None, custom_field10=None, custom_field2=None, custom_field3=None, custom_field4=None, custom_field5=None, custom_field6=None, custom_field7=None, custom_field8=None, custom_field9=None, ip_address=None, return_code=None, return_url=None, screen_branding_theme_code=None, storefront_host_name=None, user_agent=None):  # noqa: E501
        """CartCheckout - a model defined in Swagger"""  # noqa: E501

        self._comments = None
        self._current_step = None
        self._custom_field1 = None
        self._custom_field10 = None
        self._custom_field2 = None
        self._custom_field3 = None
        self._custom_field4 = None
        self._custom_field5 = None
        self._custom_field6 = None
        self._custom_field7 = None
        self._custom_field8 = None
        self._custom_field9 = None
        self._ip_address = None
        self._return_code = None
        self._return_url = None
        self._screen_branding_theme_code = None
        self._storefront_host_name = None
        self._user_agent = None
        self.discriminator = None

        if comments is not None:
            self.comments = comments
        if current_step is not None:
            self.current_step = current_step
        if custom_field1 is not None:
            self.custom_field1 = custom_field1
        if custom_field10 is not None:
            self.custom_field10 = custom_field10
        if custom_field2 is not None:
            self.custom_field2 = custom_field2
        if custom_field3 is not None:
            self.custom_field3 = custom_field3
        if custom_field4 is not None:
            self.custom_field4 = custom_field4
        if custom_field5 is not None:
            self.custom_field5 = custom_field5
        if custom_field6 is not None:
            self.custom_field6 = custom_field6
        if custom_field7 is not None:
            self.custom_field7 = custom_field7
        if custom_field8 is not None:
            self.custom_field8 = custom_field8
        if custom_field9 is not None:
            self.custom_field9 = custom_field9
        if ip_address is not None:
            self.ip_address = ip_address
        if return_code is not None:
            self.return_code = return_code
        if return_url is not None:
            self.return_url = return_url
        if screen_branding_theme_code is not None:
            self.screen_branding_theme_code = screen_branding_theme_code
        if storefront_host_name is not None:
            self.storefront_host_name = storefront_host_name
        if user_agent is not None:
            self.user_agent = user_agent

    @property
    def comments(self):
        """Gets the comments of this CartCheckout.  # noqa: E501

        Comments from the customer.  Rarely used on the single page checkout.  # noqa: E501

        :return: The comments of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """Sets the comments of this CartCheckout.

        Comments from the customer.  Rarely used on the single page checkout.  # noqa: E501

        :param comments: The comments of this CartCheckout.  # noqa: E501
        :type: str
        """
        if comments is not None and len(comments) > 2000:
            raise ValueError("Invalid value for `comments`, length must be less than or equal to `2000`")  # noqa: E501

        self._comments = comments

    @property
    def current_step(self):
        """Gets the current_step of this CartCheckout.  # noqa: E501

        Current step of the checkout (read only)  # noqa: E501

        :return: The current_step of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._current_step

    @current_step.setter
    def current_step(self, current_step):
        """Sets the current_step of this CartCheckout.

        Current step of the checkout (read only)  # noqa: E501

        :param current_step: The current_step of this CartCheckout.  # noqa: E501
        :type: str
        """

        self._current_step = current_step

    @property
    def custom_field1(self):
        """Gets the custom_field1 of this CartCheckout.  # noqa: E501

        Custom field 1  # noqa: E501

        :return: The custom_field1 of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._custom_field1

    @custom_field1.setter
    def custom_field1(self, custom_field1):
        """Sets the custom_field1 of this CartCheckout.

        Custom field 1  # noqa: E501

        :param custom_field1: The custom_field1 of this CartCheckout.  # noqa: E501
        :type: str
        """
        if custom_field1 is not None and len(custom_field1) > 50:
            raise ValueError("Invalid value for `custom_field1`, length must be less than or equal to `50`")  # noqa: E501

        self._custom_field1 = custom_field1

    @property
    def custom_field10(self):
        """Gets the custom_field10 of this CartCheckout.  # noqa: E501

        Custom field 10  # noqa: E501

        :return: The custom_field10 of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._custom_field10

    @custom_field10.setter
    def custom_field10(self, custom_field10):
        """Sets the custom_field10 of this CartCheckout.

        Custom field 10  # noqa: E501

        :param custom_field10: The custom_field10 of this CartCheckout.  # noqa: E501
        :type: str
        """
        if custom_field10 is not None and len(custom_field10) > 200:
            raise ValueError("Invalid value for `custom_field10`, length must be less than or equal to `200`")  # noqa: E501

        self._custom_field10 = custom_field10

    @property
    def custom_field2(self):
        """Gets the custom_field2 of this CartCheckout.  # noqa: E501

        Custom field 2  # noqa: E501

        :return: The custom_field2 of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._custom_field2

    @custom_field2.setter
    def custom_field2(self, custom_field2):
        """Sets the custom_field2 of this CartCheckout.

        Custom field 2  # noqa: E501

        :param custom_field2: The custom_field2 of this CartCheckout.  # noqa: E501
        :type: str
        """
        if custom_field2 is not None and len(custom_field2) > 50:
            raise ValueError("Invalid value for `custom_field2`, length must be less than or equal to `50`")  # noqa: E501

        self._custom_field2 = custom_field2

    @property
    def custom_field3(self):
        """Gets the custom_field3 of this CartCheckout.  # noqa: E501

        Custom field 3  # noqa: E501

        :return: The custom_field3 of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._custom_field3

    @custom_field3.setter
    def custom_field3(self, custom_field3):
        """Sets the custom_field3 of this CartCheckout.

        Custom field 3  # noqa: E501

        :param custom_field3: The custom_field3 of this CartCheckout.  # noqa: E501
        :type: str
        """
        if custom_field3 is not None and len(custom_field3) > 50:
            raise ValueError("Invalid value for `custom_field3`, length must be less than or equal to `50`")  # noqa: E501

        self._custom_field3 = custom_field3

    @property
    def custom_field4(self):
        """Gets the custom_field4 of this CartCheckout.  # noqa: E501

        Custom field 4  # noqa: E501

        :return: The custom_field4 of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._custom_field4

    @custom_field4.setter
    def custom_field4(self, custom_field4):
        """Sets the custom_field4 of this CartCheckout.

        Custom field 4  # noqa: E501

        :param custom_field4: The custom_field4 of this CartCheckout.  # noqa: E501
        :type: str
        """
        if custom_field4 is not None and len(custom_field4) > 50:
            raise ValueError("Invalid value for `custom_field4`, length must be less than or equal to `50`")  # noqa: E501

        self._custom_field4 = custom_field4

    @property
    def custom_field5(self):
        """Gets the custom_field5 of this CartCheckout.  # noqa: E501

        Custom field 5  # noqa: E501

        :return: The custom_field5 of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._custom_field5

    @custom_field5.setter
    def custom_field5(self, custom_field5):
        """Sets the custom_field5 of this CartCheckout.

        Custom field 5  # noqa: E501

        :param custom_field5: The custom_field5 of this CartCheckout.  # noqa: E501
        :type: str
        """
        if custom_field5 is not None and len(custom_field5) > 75:
            raise ValueError("Invalid value for `custom_field5`, length must be less than or equal to `75`")  # noqa: E501

        self._custom_field5 = custom_field5

    @property
    def custom_field6(self):
        """Gets the custom_field6 of this CartCheckout.  # noqa: E501

        Custom field 6  # noqa: E501

        :return: The custom_field6 of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._custom_field6

    @custom_field6.setter
    def custom_field6(self, custom_field6):
        """Sets the custom_field6 of this CartCheckout.

        Custom field 6  # noqa: E501

        :param custom_field6: The custom_field6 of this CartCheckout.  # noqa: E501
        :type: str
        """
        if custom_field6 is not None and len(custom_field6) > 50:
            raise ValueError("Invalid value for `custom_field6`, length must be less than or equal to `50`")  # noqa: E501

        self._custom_field6 = custom_field6

    @property
    def custom_field7(self):
        """Gets the custom_field7 of this CartCheckout.  # noqa: E501

        Custom field 7  # noqa: E501

        :return: The custom_field7 of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._custom_field7

    @custom_field7.setter
    def custom_field7(self, custom_field7):
        """Sets the custom_field7 of this CartCheckout.

        Custom field 7  # noqa: E501

        :param custom_field7: The custom_field7 of this CartCheckout.  # noqa: E501
        :type: str
        """
        if custom_field7 is not None and len(custom_field7) > 50:
            raise ValueError("Invalid value for `custom_field7`, length must be less than or equal to `50`")  # noqa: E501

        self._custom_field7 = custom_field7

    @property
    def custom_field8(self):
        """Gets the custom_field8 of this CartCheckout.  # noqa: E501

        Custom field 8  # noqa: E501

        :return: The custom_field8 of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._custom_field8

    @custom_field8.setter
    def custom_field8(self, custom_field8):
        """Sets the custom_field8 of this CartCheckout.

        Custom field 8  # noqa: E501

        :param custom_field8: The custom_field8 of this CartCheckout.  # noqa: E501
        :type: str
        """
        if custom_field8 is not None and len(custom_field8) > 200:
            raise ValueError("Invalid value for `custom_field8`, length must be less than or equal to `200`")  # noqa: E501

        self._custom_field8 = custom_field8

    @property
    def custom_field9(self):
        """Gets the custom_field9 of this CartCheckout.  # noqa: E501

        Custom field 9  # noqa: E501

        :return: The custom_field9 of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._custom_field9

    @custom_field9.setter
    def custom_field9(self, custom_field9):
        """Sets the custom_field9 of this CartCheckout.

        Custom field 9  # noqa: E501

        :param custom_field9: The custom_field9 of this CartCheckout.  # noqa: E501
        :type: str
        """
        if custom_field9 is not None and len(custom_field9) > 200:
            raise ValueError("Invalid value for `custom_field9`, length must be less than or equal to `200`")  # noqa: E501

        self._custom_field9 = custom_field9

    @property
    def ip_address(self):
        """Gets the ip_address of this CartCheckout.  # noqa: E501

        IP Address (read only unless non-browser key authenticated)  # noqa: E501

        :return: The ip_address of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        """Sets the ip_address of this CartCheckout.

        IP Address (read only unless non-browser key authenticated)  # noqa: E501

        :param ip_address: The ip_address of this CartCheckout.  # noqa: E501
        :type: str
        """

        self._ip_address = ip_address

    @property
    def return_code(self):
        """Gets the return_code of this CartCheckout.  # noqa: E501

        Return code assigned for send return email operation  # noqa: E501

        :return: The return_code of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._return_code

    @return_code.setter
    def return_code(self, return_code):
        """Sets the return_code of this CartCheckout.

        Return code assigned for send return email operation  # noqa: E501

        :param return_code: The return_code of this CartCheckout.  # noqa: E501
        :type: str
        """

        self._return_code = return_code

    @property
    def return_url(self):
        """Gets the return_url of this CartCheckout.  # noqa: E501

        The URL to redirect the customer to when they return from an abandon cart email.  Must be https protocol.  # noqa: E501

        :return: The return_url of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._return_url

    @return_url.setter
    def return_url(self, return_url):
        """Sets the return_url of this CartCheckout.

        The URL to redirect the customer to when they return from an abandon cart email.  Must be https protocol.  # noqa: E501

        :param return_url: The return_url of this CartCheckout.  # noqa: E501
        :type: str
        """
        if return_url is not None and len(return_url) > 2048:
            raise ValueError("Invalid value for `return_url`, length must be less than or equal to `2048`")  # noqa: E501

        self._return_url = return_url

    @property
    def screen_branding_theme_code(self):
        """Gets the screen_branding_theme_code of this CartCheckout.  # noqa: E501

        Screen branding theme code  # noqa: E501

        :return: The screen_branding_theme_code of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._screen_branding_theme_code

    @screen_branding_theme_code.setter
    def screen_branding_theme_code(self, screen_branding_theme_code):
        """Sets the screen_branding_theme_code of this CartCheckout.

        Screen branding theme code  # noqa: E501

        :param screen_branding_theme_code: The screen_branding_theme_code of this CartCheckout.  # noqa: E501
        :type: str
        """
        if screen_branding_theme_code is not None and len(screen_branding_theme_code) > 10:
            raise ValueError("Invalid value for `screen_branding_theme_code`, length must be less than or equal to `10`")  # noqa: E501

        self._screen_branding_theme_code = screen_branding_theme_code

    @property
    def storefront_host_name(self):
        """Gets the storefront_host_name of this CartCheckout.  # noqa: E501

        StoreFront Host Name  # noqa: E501

        :return: The storefront_host_name of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._storefront_host_name

    @storefront_host_name.setter
    def storefront_host_name(self, storefront_host_name):
        """Sets the storefront_host_name of this CartCheckout.

        StoreFront Host Name  # noqa: E501

        :param storefront_host_name: The storefront_host_name of this CartCheckout.  # noqa: E501
        :type: str
        """

        self._storefront_host_name = storefront_host_name

    @property
    def user_agent(self):
        """Gets the user_agent of this CartCheckout.  # noqa: E501

        User agent of the browser  # noqa: E501

        :return: The user_agent of this CartCheckout.  # noqa: E501
        :rtype: str
        """
        return self._user_agent

    @user_agent.setter
    def user_agent(self, user_agent):
        """Sets the user_agent of this CartCheckout.

        User agent of the browser  # noqa: E501

        :param user_agent: The user_agent of this CartCheckout.  # noqa: E501
        :type: str
        """

        self._user_agent = user_agent

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
        if issubclass(CartCheckout, dict):
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
        if not isinstance(other, CartCheckout):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
