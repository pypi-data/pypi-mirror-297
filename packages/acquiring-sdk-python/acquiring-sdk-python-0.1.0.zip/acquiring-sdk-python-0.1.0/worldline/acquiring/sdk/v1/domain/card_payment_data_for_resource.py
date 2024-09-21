# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from .point_of_sale_data import PointOfSaleData

from worldline.acquiring.sdk.domain.data_object import DataObject


class CardPaymentDataForResource(DataObject):

    __brand: Optional[str] = None
    __point_of_sale_data: Optional[PointOfSaleData] = None

    @property
    def brand(self) -> Optional[str]:
        """
        | The card brand

        Type: str
        """
        return self.__brand

    @brand.setter
    def brand(self, value: Optional[str]) -> None:
        self.__brand = value

    @property
    def point_of_sale_data(self) -> Optional[PointOfSaleData]:
        """
        | Payment terminal request data

        Type: :class:`worldline.acquiring.sdk.v1.domain.point_of_sale_data.PointOfSaleData`
        """
        return self.__point_of_sale_data

    @point_of_sale_data.setter
    def point_of_sale_data(self, value: Optional[PointOfSaleData]) -> None:
        self.__point_of_sale_data = value

    def to_dictionary(self) -> dict:
        dictionary = super(CardPaymentDataForResource, self).to_dictionary()
        if self.brand is not None:
            dictionary['brand'] = self.brand
        if self.point_of_sale_data is not None:
            dictionary['pointOfSaleData'] = self.point_of_sale_data.to_dictionary()
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'CardPaymentDataForResource':
        super(CardPaymentDataForResource, self).from_dictionary(dictionary)
        if 'brand' in dictionary:
            self.brand = dictionary['brand']
        if 'pointOfSaleData' in dictionary:
            if not isinstance(dictionary['pointOfSaleData'], dict):
                raise TypeError('value \'{}\' is not a dictionary'.format(dictionary['pointOfSaleData']))
            value = PointOfSaleData()
            self.point_of_sale_data = value.from_dictionary(dictionary['pointOfSaleData'])
        return self
