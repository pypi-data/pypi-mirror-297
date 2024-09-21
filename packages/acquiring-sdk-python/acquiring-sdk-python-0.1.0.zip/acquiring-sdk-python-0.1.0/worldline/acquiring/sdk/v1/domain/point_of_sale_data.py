# -*- coding: utf-8 -*-
#
# This file was automatically generated.
#
from typing import Optional

from worldline.acquiring.sdk.domain.data_object import DataObject


class PointOfSaleData(DataObject):

    __terminal_id: Optional[str] = None

    @property
    def terminal_id(self) -> Optional[str]:
        """
        | Terminal ID ANS(8)

        Type: str
        """
        return self.__terminal_id

    @terminal_id.setter
    def terminal_id(self, value: Optional[str]) -> None:
        self.__terminal_id = value

    def to_dictionary(self) -> dict:
        dictionary = super(PointOfSaleData, self).to_dictionary()
        if self.terminal_id is not None:
            dictionary['terminalId'] = self.terminal_id
        return dictionary

    def from_dictionary(self, dictionary: dict) -> 'PointOfSaleData':
        super(PointOfSaleData, self).from_dictionary(dictionary)
        if 'terminalId' in dictionary:
            self.terminal_id = dictionary['terminalId']
        return self
