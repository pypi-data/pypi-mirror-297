# -*- coding: utf-8 -*-
# File generated from our OpenAPI spec
from stripe._list_object import ListObject
from stripe._request_options import RequestOptions
from stripe._stripe_service import StripeService
from stripe._util import sanitize_id
from stripe.tax._calculation_line_item import CalculationLineItem
from typing import List, cast
from typing_extensions import NotRequired, TypedDict


class CalculationLineItemService(StripeService):
    class ListParams(TypedDict):
        ending_before: NotRequired[str]
        """
        A cursor for use in pagination. `ending_before` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, starting with `obj_bar`, your subsequent call can include `ending_before=obj_bar` in order to fetch the previous page of the list.
        """
        expand: NotRequired[List[str]]
        """
        Specifies which fields in the response should be expanded.
        """
        limit: NotRequired[int]
        """
        A limit on the number of objects to be returned. Limit can range between 1 and 100, and the default is 10.
        """
        starting_after: NotRequired[str]
        """
        A cursor for use in pagination. `starting_after` is an object ID that defines your place in the list. For instance, if you make a list request and receive 100 objects, ending with `obj_foo`, your subsequent call can include `starting_after=obj_foo` in order to fetch the next page of the list.
        """

    def list(
        self,
        calculation: str,
        params: "CalculationLineItemService.ListParams" = {},
        options: RequestOptions = {},
    ) -> ListObject[CalculationLineItem]:
        """
        Retrieves the line items of a tax calculation as a collection, if the calculation hasn't expired.
        """
        return cast(
            ListObject[CalculationLineItem],
            self._request(
                "get",
                "/v1/tax/calculations/{calculation}/line_items".format(
                    calculation=sanitize_id(calculation),
                ),
                base_address="api",
                params=params,
                options=options,
            ),
        )

    async def list_async(
        self,
        calculation: str,
        params: "CalculationLineItemService.ListParams" = {},
        options: RequestOptions = {},
    ) -> ListObject[CalculationLineItem]:
        """
        Retrieves the line items of a tax calculation as a collection, if the calculation hasn't expired.
        """
        return cast(
            ListObject[CalculationLineItem],
            await self._request_async(
                "get",
                "/v1/tax/calculations/{calculation}/line_items".format(
                    calculation=sanitize_id(calculation),
                ),
                base_address="api",
                params=params,
                options=options,
            ),
        )
