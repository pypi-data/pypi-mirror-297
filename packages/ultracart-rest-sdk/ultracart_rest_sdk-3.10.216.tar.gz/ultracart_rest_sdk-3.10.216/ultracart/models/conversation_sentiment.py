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


class ConversationSentiment(object):
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
        'last_detect_sentiment': 'str',
        'mixed': 'float',
        'negative': 'float',
        'neutral': 'float',
        'positive': 'float',
        'sentiment': 'str'
    }

    attribute_map = {
        'last_detect_sentiment': 'last_detect_sentiment',
        'mixed': 'mixed',
        'negative': 'negative',
        'neutral': 'neutral',
        'positive': 'positive',
        'sentiment': 'sentiment'
    }

    def __init__(self, last_detect_sentiment=None, mixed=None, negative=None, neutral=None, positive=None, sentiment=None):  # noqa: E501
        """ConversationSentiment - a model defined in Swagger"""  # noqa: E501

        self._last_detect_sentiment = None
        self._mixed = None
        self._negative = None
        self._neutral = None
        self._positive = None
        self._sentiment = None
        self.discriminator = None

        if last_detect_sentiment is not None:
            self.last_detect_sentiment = last_detect_sentiment
        if mixed is not None:
            self.mixed = mixed
        if negative is not None:
            self.negative = negative
        if neutral is not None:
            self.neutral = neutral
        if positive is not None:
            self.positive = positive
        if sentiment is not None:
            self.sentiment = sentiment

    @property
    def last_detect_sentiment(self):
        """Gets the last_detect_sentiment of this ConversationSentiment.  # noqa: E501

        The last time the detect sentiment was run on this conversation  # noqa: E501

        :return: The last_detect_sentiment of this ConversationSentiment.  # noqa: E501
        :rtype: str
        """
        return self._last_detect_sentiment

    @last_detect_sentiment.setter
    def last_detect_sentiment(self, last_detect_sentiment):
        """Sets the last_detect_sentiment of this ConversationSentiment.

        The last time the detect sentiment was run on this conversation  # noqa: E501

        :param last_detect_sentiment: The last_detect_sentiment of this ConversationSentiment.  # noqa: E501
        :type: str
        """

        self._last_detect_sentiment = last_detect_sentiment

    @property
    def mixed(self):
        """Gets the mixed of this ConversationSentiment.  # noqa: E501

        The mixed score  # noqa: E501

        :return: The mixed of this ConversationSentiment.  # noqa: E501
        :rtype: float
        """
        return self._mixed

    @mixed.setter
    def mixed(self, mixed):
        """Sets the mixed of this ConversationSentiment.

        The mixed score  # noqa: E501

        :param mixed: The mixed of this ConversationSentiment.  # noqa: E501
        :type: float
        """

        self._mixed = mixed

    @property
    def negative(self):
        """Gets the negative of this ConversationSentiment.  # noqa: E501

        The negative score  # noqa: E501

        :return: The negative of this ConversationSentiment.  # noqa: E501
        :rtype: float
        """
        return self._negative

    @negative.setter
    def negative(self, negative):
        """Sets the negative of this ConversationSentiment.

        The negative score  # noqa: E501

        :param negative: The negative of this ConversationSentiment.  # noqa: E501
        :type: float
        """

        self._negative = negative

    @property
    def neutral(self):
        """Gets the neutral of this ConversationSentiment.  # noqa: E501

        The neutral score  # noqa: E501

        :return: The neutral of this ConversationSentiment.  # noqa: E501
        :rtype: float
        """
        return self._neutral

    @neutral.setter
    def neutral(self, neutral):
        """Sets the neutral of this ConversationSentiment.

        The neutral score  # noqa: E501

        :param neutral: The neutral of this ConversationSentiment.  # noqa: E501
        :type: float
        """

        self._neutral = neutral

    @property
    def positive(self):
        """Gets the positive of this ConversationSentiment.  # noqa: E501

        The positive score  # noqa: E501

        :return: The positive of this ConversationSentiment.  # noqa: E501
        :rtype: float
        """
        return self._positive

    @positive.setter
    def positive(self, positive):
        """Sets the positive of this ConversationSentiment.

        The positive score  # noqa: E501

        :param positive: The positive of this ConversationSentiment.  # noqa: E501
        :type: float
        """

        self._positive = positive

    @property
    def sentiment(self):
        """Gets the sentiment of this ConversationSentiment.  # noqa: E501

        The overall sentiment  # noqa: E501

        :return: The sentiment of this ConversationSentiment.  # noqa: E501
        :rtype: str
        """
        return self._sentiment

    @sentiment.setter
    def sentiment(self, sentiment):
        """Sets the sentiment of this ConversationSentiment.

        The overall sentiment  # noqa: E501

        :param sentiment: The sentiment of this ConversationSentiment.  # noqa: E501
        :type: str
        """
        allowed_values = ["POSITIVE", "NEUTRAL", "NEGATIVE", "MIXED"]  # noqa: E501
        if sentiment not in allowed_values:
            raise ValueError(
                "Invalid value for `sentiment` ({0}), must be one of {1}"  # noqa: E501
                .format(sentiment, allowed_values)
            )

        self._sentiment = sentiment

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
        if issubclass(ConversationSentiment, dict):
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
        if not isinstance(other, ConversationSentiment):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
