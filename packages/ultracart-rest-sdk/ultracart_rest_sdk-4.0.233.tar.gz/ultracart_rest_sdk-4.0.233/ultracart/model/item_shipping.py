"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from ultracart.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
    OpenApiModel
)
from ultracart.exceptions import ApiAttributeError


def lazy_import():
    from ultracart.model.distance import Distance
    from ultracart.model.item_shipping_case import ItemShippingCase
    from ultracart.model.item_shipping_destination_markup import ItemShippingDestinationMarkup
    from ultracart.model.item_shipping_destination_restriction import ItemShippingDestinationRestriction
    from ultracart.model.item_shipping_distribution_center import ItemShippingDistributionCenter
    from ultracart.model.item_shipping_method import ItemShippingMethod
    from ultracart.model.item_shipping_package_requirement import ItemShippingPackageRequirement
    from ultracart.model.weight import Weight
    globals()['Distance'] = Distance
    globals()['ItemShippingCase'] = ItemShippingCase
    globals()['ItemShippingDestinationMarkup'] = ItemShippingDestinationMarkup
    globals()['ItemShippingDestinationRestriction'] = ItemShippingDestinationRestriction
    globals()['ItemShippingDistributionCenter'] = ItemShippingDistributionCenter
    globals()['ItemShippingMethod'] = ItemShippingMethod
    globals()['ItemShippingPackageRequirement'] = ItemShippingPackageRequirement
    globals()['Weight'] = Weight


class ItemShipping(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
        ('country_code_of_origin',): {
            'max_length': 2,
        },
    }

    @cached_property
    def additional_properties_type():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded
        """
        lazy_import()
        return (bool, date, datetime, dict, float, int, list, str, none_type,)  # noqa: E501

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        lazy_import()
        return {
            'allow_back_order': (bool,),  # noqa: E501
            'amazon_fba': (bool,),  # noqa: E501
            'case_inner_packs': (int,),  # noqa: E501
            'case_units': (int,),  # noqa: E501
            'cases': ([ItemShippingCase],),  # noqa: E501
            'collect_serial_numbers': (bool,),  # noqa: E501
            'country_code_of_origin': (str,),  # noqa: E501
            'customs_description': (str,),  # noqa: E501
            'customs_value': (float,),  # noqa: E501
            'delivery_on_friday': (bool,),  # noqa: E501
            'delivery_on_monday': (bool,),  # noqa: E501
            'delivery_on_saturday': (bool,),  # noqa: E501
            'delivery_on_sunday': (bool,),  # noqa: E501
            'delivery_on_thursday': (bool,),  # noqa: E501
            'delivery_on_tuesday': (bool,),  # noqa: E501
            'delivery_on_wednesday': (bool,),  # noqa: E501
            'destination_markups': ([ItemShippingDestinationMarkup],),  # noqa: E501
            'destination_restrictions': ([ItemShippingDestinationRestriction],),  # noqa: E501
            'distribution_centers': ([ItemShippingDistributionCenter],),  # noqa: E501
            'eta': (str,),  # noqa: E501
            'free_shipping': (bool,),  # noqa: E501
            'freight_class': (str,),  # noqa: E501
            'hazmat': (bool,),  # noqa: E501
            'hold_for_transmission': (bool,),  # noqa: E501
            'made_to_order': (bool,),  # noqa: E501
            'made_to_order_lead_time': (int,),  # noqa: E501
            'max_days_time_in_transit': (int,),  # noqa: E501
            'methods': ([ItemShippingMethod],),  # noqa: E501
            'no_shipping_discount': (bool,),  # noqa: E501
            'package_requirements': ([ItemShippingPackageRequirement],),  # noqa: E501
            'perishable_class_name': (str,),  # noqa: E501
            'perishable_class_oid': (int,),  # noqa: E501
            'preorder': (bool,),  # noqa: E501
            'require_delivery_date': (bool,),  # noqa: E501
            'restrict_shipment_on_friday': (bool,),  # noqa: E501
            'restrict_shipment_on_monday': (bool,),  # noqa: E501
            'restrict_shipment_on_saturday': (bool,),  # noqa: E501
            'restrict_shipment_on_sunday': (bool,),  # noqa: E501
            'restrict_shipment_on_thursday': (bool,),  # noqa: E501
            'restrict_shipment_on_tuesday': (bool,),  # noqa: E501
            'restrict_shipment_on_wednesday': (bool,),  # noqa: E501
            'ship_separately': (bool,),  # noqa: E501
            'ship_separately_additional_weight': (Weight,),  # noqa: E501
            'ship_separately_height': (Distance,),  # noqa: E501
            'ship_separately_length': (Distance,),  # noqa: E501
            'ship_separately_package_special_type': (str,),  # noqa: E501
            'ship_separately_width': (Distance,),  # noqa: E501
            'special_product_type': (str,),  # noqa: E501
            'track_inventory': (bool,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'allow_back_order': 'allow_back_order',  # noqa: E501
        'amazon_fba': 'amazon_fba',  # noqa: E501
        'case_inner_packs': 'case_inner_packs',  # noqa: E501
        'case_units': 'case_units',  # noqa: E501
        'cases': 'cases',  # noqa: E501
        'collect_serial_numbers': 'collect_serial_numbers',  # noqa: E501
        'country_code_of_origin': 'country_code_of_origin',  # noqa: E501
        'customs_description': 'customs_description',  # noqa: E501
        'customs_value': 'customs_value',  # noqa: E501
        'delivery_on_friday': 'delivery_on_friday',  # noqa: E501
        'delivery_on_monday': 'delivery_on_monday',  # noqa: E501
        'delivery_on_saturday': 'delivery_on_saturday',  # noqa: E501
        'delivery_on_sunday': 'delivery_on_sunday',  # noqa: E501
        'delivery_on_thursday': 'delivery_on_thursday',  # noqa: E501
        'delivery_on_tuesday': 'delivery_on_tuesday',  # noqa: E501
        'delivery_on_wednesday': 'delivery_on_wednesday',  # noqa: E501
        'destination_markups': 'destination_markups',  # noqa: E501
        'destination_restrictions': 'destination_restrictions',  # noqa: E501
        'distribution_centers': 'distribution_centers',  # noqa: E501
        'eta': 'eta',  # noqa: E501
        'free_shipping': 'free_shipping',  # noqa: E501
        'freight_class': 'freight_class',  # noqa: E501
        'hazmat': 'hazmat',  # noqa: E501
        'hold_for_transmission': 'hold_for_transmission',  # noqa: E501
        'made_to_order': 'made_to_order',  # noqa: E501
        'made_to_order_lead_time': 'made_to_order_lead_time',  # noqa: E501
        'max_days_time_in_transit': 'max_days_time_in_transit',  # noqa: E501
        'methods': 'methods',  # noqa: E501
        'no_shipping_discount': 'no_shipping_discount',  # noqa: E501
        'package_requirements': 'package_requirements',  # noqa: E501
        'perishable_class_name': 'perishable_class_name',  # noqa: E501
        'perishable_class_oid': 'perishable_class_oid',  # noqa: E501
        'preorder': 'preorder',  # noqa: E501
        'require_delivery_date': 'require_delivery_date',  # noqa: E501
        'restrict_shipment_on_friday': 'restrict_shipment_on_friday',  # noqa: E501
        'restrict_shipment_on_monday': 'restrict_shipment_on_monday',  # noqa: E501
        'restrict_shipment_on_saturday': 'restrict_shipment_on_saturday',  # noqa: E501
        'restrict_shipment_on_sunday': 'restrict_shipment_on_sunday',  # noqa: E501
        'restrict_shipment_on_thursday': 'restrict_shipment_on_thursday',  # noqa: E501
        'restrict_shipment_on_tuesday': 'restrict_shipment_on_tuesday',  # noqa: E501
        'restrict_shipment_on_wednesday': 'restrict_shipment_on_wednesday',  # noqa: E501
        'ship_separately': 'ship_separately',  # noqa: E501
        'ship_separately_additional_weight': 'ship_separately_additional_weight',  # noqa: E501
        'ship_separately_height': 'ship_separately_height',  # noqa: E501
        'ship_separately_length': 'ship_separately_length',  # noqa: E501
        'ship_separately_package_special_type': 'ship_separately_package_special_type',  # noqa: E501
        'ship_separately_width': 'ship_separately_width',  # noqa: E501
        'special_product_type': 'special_product_type',  # noqa: E501
        'track_inventory': 'track_inventory',  # noqa: E501
    }

    read_only_vars = {
    }

    _composed_schemas = {}

    @classmethod
    @convert_js_args_to_python_args
    def _from_openapi_data(cls, *args, **kwargs):  # noqa: E501
        """ItemShipping - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            allow_back_order (bool): Allow back order. [optional]  # noqa: E501
            amazon_fba (bool): Fulfillment by Amazon.com. [optional]  # noqa: E501
            case_inner_packs (int): Case inner packs. [optional]  # noqa: E501
            case_units (int): Case units. [optional]  # noqa: E501
            cases ([ItemShippingCase]): Cases. [optional]  # noqa: E501
            collect_serial_numbers (bool): This item is on pre-order. [optional]  # noqa: E501
            country_code_of_origin (str): Country code of origin for customs forms.  (ISO-3166 two letter code). [optional]  # noqa: E501
            customs_description (str): Customs description. [optional]  # noqa: E501
            customs_value (float): Customs value. [optional]  # noqa: E501
            delivery_on_friday (bool): Delivery on Friday. [optional]  # noqa: E501
            delivery_on_monday (bool): Delivery on Monday. [optional]  # noqa: E501
            delivery_on_saturday (bool): Delivery on Saturday. [optional]  # noqa: E501
            delivery_on_sunday (bool): Delivery on Sunday. [optional]  # noqa: E501
            delivery_on_thursday (bool): Delivery on Thursday. [optional]  # noqa: E501
            delivery_on_tuesday (bool): Delivery on Tuesday. [optional]  # noqa: E501
            delivery_on_wednesday (bool): Delivery on Wednesday. [optional]  # noqa: E501
            destination_markups ([ItemShippingDestinationMarkup]): Destination markups. [optional]  # noqa: E501
            destination_restrictions ([ItemShippingDestinationRestriction]): Destination restrictions. [optional]  # noqa: E501
            distribution_centers ([ItemShippingDistributionCenter]): Distribution centers. [optional]  # noqa: E501
            eta (str): Estimated time of arrival. [optional]  # noqa: E501
            free_shipping (bool): Qualifies for free shipping. [optional]  # noqa: E501
            freight_class (str): Freight class. [optional]  # noqa: E501
            hazmat (bool): Hazardous material. [optional]  # noqa: E501
            hold_for_transmission (bool): Hold for transmission. [optional]  # noqa: E501
            made_to_order (bool): True if this item is made to order. [optional]  # noqa: E501
            made_to_order_lead_time (int): Number of days lead time it takes to make the item before ite can ship. [optional]  # noqa: E501
            max_days_time_in_transit (int): Maximum days allowed in transit. [optional]  # noqa: E501
            methods ([ItemShippingMethod]): Methods. [optional]  # noqa: E501
            no_shipping_discount (bool): No shipping discounts. [optional]  # noqa: E501
            package_requirements ([ItemShippingPackageRequirement]): Package requirements. [optional]  # noqa: E501
            perishable_class_name (str): Perishable class name. [optional]  # noqa: E501
            perishable_class_oid (int): Perishable class object identifier. [optional]  # noqa: E501
            preorder (bool): This item is on pre-order. [optional]  # noqa: E501
            require_delivery_date (bool): True to require customer to select a delivery date. [optional]  # noqa: E501
            restrict_shipment_on_friday (bool): Restrict shipment on Friday. [optional]  # noqa: E501
            restrict_shipment_on_monday (bool): Restrict shipment on Monday. [optional]  # noqa: E501
            restrict_shipment_on_saturday (bool): Restrict shipment on Saturday. [optional]  # noqa: E501
            restrict_shipment_on_sunday (bool): Restrict shipment on Sunday. [optional]  # noqa: E501
            restrict_shipment_on_thursday (bool): Restrict shipment on Thursday. [optional]  # noqa: E501
            restrict_shipment_on_tuesday (bool): Restrict shipment on Tuesday. [optional]  # noqa: E501
            restrict_shipment_on_wednesday (bool): Restrict shipment on Wednesday. [optional]  # noqa: E501
            ship_separately (bool): Ship this item in a separate box. [optional]  # noqa: E501
            ship_separately_additional_weight (Weight): [optional]  # noqa: E501
            ship_separately_height (Distance): [optional]  # noqa: E501
            ship_separately_length (Distance): [optional]  # noqa: E501
            ship_separately_package_special_type (str): Ship separately package special type. [optional]  # noqa: E501
            ship_separately_width (Distance): [optional]  # noqa: E501
            special_product_type (str): Special product type (USPS Media Mail). [optional]  # noqa: E501
            track_inventory (bool): Track inventory. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', True)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        self = super(OpenApiModel, cls).__new__(cls)

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
        return self

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, *args, **kwargs):  # noqa: E501
        """ItemShipping - a model defined in OpenAPI

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            allow_back_order (bool): Allow back order. [optional]  # noqa: E501
            amazon_fba (bool): Fulfillment by Amazon.com. [optional]  # noqa: E501
            case_inner_packs (int): Case inner packs. [optional]  # noqa: E501
            case_units (int): Case units. [optional]  # noqa: E501
            cases ([ItemShippingCase]): Cases. [optional]  # noqa: E501
            collect_serial_numbers (bool): This item is on pre-order. [optional]  # noqa: E501
            country_code_of_origin (str): Country code of origin for customs forms.  (ISO-3166 two letter code). [optional]  # noqa: E501
            customs_description (str): Customs description. [optional]  # noqa: E501
            customs_value (float): Customs value. [optional]  # noqa: E501
            delivery_on_friday (bool): Delivery on Friday. [optional]  # noqa: E501
            delivery_on_monday (bool): Delivery on Monday. [optional]  # noqa: E501
            delivery_on_saturday (bool): Delivery on Saturday. [optional]  # noqa: E501
            delivery_on_sunday (bool): Delivery on Sunday. [optional]  # noqa: E501
            delivery_on_thursday (bool): Delivery on Thursday. [optional]  # noqa: E501
            delivery_on_tuesday (bool): Delivery on Tuesday. [optional]  # noqa: E501
            delivery_on_wednesday (bool): Delivery on Wednesday. [optional]  # noqa: E501
            destination_markups ([ItemShippingDestinationMarkup]): Destination markups. [optional]  # noqa: E501
            destination_restrictions ([ItemShippingDestinationRestriction]): Destination restrictions. [optional]  # noqa: E501
            distribution_centers ([ItemShippingDistributionCenter]): Distribution centers. [optional]  # noqa: E501
            eta (str): Estimated time of arrival. [optional]  # noqa: E501
            free_shipping (bool): Qualifies for free shipping. [optional]  # noqa: E501
            freight_class (str): Freight class. [optional]  # noqa: E501
            hazmat (bool): Hazardous material. [optional]  # noqa: E501
            hold_for_transmission (bool): Hold for transmission. [optional]  # noqa: E501
            made_to_order (bool): True if this item is made to order. [optional]  # noqa: E501
            made_to_order_lead_time (int): Number of days lead time it takes to make the item before ite can ship. [optional]  # noqa: E501
            max_days_time_in_transit (int): Maximum days allowed in transit. [optional]  # noqa: E501
            methods ([ItemShippingMethod]): Methods. [optional]  # noqa: E501
            no_shipping_discount (bool): No shipping discounts. [optional]  # noqa: E501
            package_requirements ([ItemShippingPackageRequirement]): Package requirements. [optional]  # noqa: E501
            perishable_class_name (str): Perishable class name. [optional]  # noqa: E501
            perishable_class_oid (int): Perishable class object identifier. [optional]  # noqa: E501
            preorder (bool): This item is on pre-order. [optional]  # noqa: E501
            require_delivery_date (bool): True to require customer to select a delivery date. [optional]  # noqa: E501
            restrict_shipment_on_friday (bool): Restrict shipment on Friday. [optional]  # noqa: E501
            restrict_shipment_on_monday (bool): Restrict shipment on Monday. [optional]  # noqa: E501
            restrict_shipment_on_saturday (bool): Restrict shipment on Saturday. [optional]  # noqa: E501
            restrict_shipment_on_sunday (bool): Restrict shipment on Sunday. [optional]  # noqa: E501
            restrict_shipment_on_thursday (bool): Restrict shipment on Thursday. [optional]  # noqa: E501
            restrict_shipment_on_tuesday (bool): Restrict shipment on Tuesday. [optional]  # noqa: E501
            restrict_shipment_on_wednesday (bool): Restrict shipment on Wednesday. [optional]  # noqa: E501
            ship_separately (bool): Ship this item in a separate box. [optional]  # noqa: E501
            ship_separately_additional_weight (Weight): [optional]  # noqa: E501
            ship_separately_height (Distance): [optional]  # noqa: E501
            ship_separately_length (Distance): [optional]  # noqa: E501
            ship_separately_package_special_type (str): Ship separately package special type. [optional]  # noqa: E501
            ship_separately_width (Distance): [optional]  # noqa: E501
            special_product_type (str): Special product type (USPS Media Mail). [optional]  # noqa: E501
            track_inventory (bool): Track inventory. [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            for arg in args:
                if isinstance(arg, dict):
                    kwargs.update(arg)
                else:
                    raise ApiTypeError(
                        "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                            args,
                            self.__class__.__name__,
                        ),
                        path_to_item=_path_to_item,
                        valid_classes=(self.__class__,),
                    )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
            if var_name in self.read_only_vars:
                raise ApiAttributeError(f"`{var_name}` is a read-only attribute. Use `from_openapi_data` to instantiate "
                                     f"class with read only attributes.")
