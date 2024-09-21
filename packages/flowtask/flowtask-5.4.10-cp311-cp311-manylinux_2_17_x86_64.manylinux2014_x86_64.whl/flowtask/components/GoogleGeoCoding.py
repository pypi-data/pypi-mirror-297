from collections.abc import Callable
import asyncio
import aiohttp
import logging
import pandas as pd
from flowtask.conf import GOOGLE_API_KEY
from flowtask.components import DtComponent
from flowtask.exceptions import ComponentError


logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


class GoogleGeoCoding(DtComponent):
    base_url: str = "https://maps.googleapis.com/maps/api/geocode/json"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.check_field = kwargs.get('comparison_field', 'formatted_address')
        self.return_pluscode: bool = kwargs.get('return_pluscode', False)
        self.place_prefix: str = kwargs.get('place_prefix', None)
        super(GoogleGeoCoding, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.semaphore = asyncio.Semaphore(10)  # Adjust the limit as needed

    async def start(self, **kwargs):
        self._counter: int = 0
        if self.previous:
            self.data = self.input
        if not hasattr(self, 'columns'):
            raise RuntimeError(
                'GoogleGeoCoding requires a Column Attribute'
            )
        if not isinstance(self.columns, list):
            raise RuntimeError(
                'GoogleGeoCoding requires a Column Attribute as list'
            )
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Incompatible Pandas Dataframe", code=404
            )
        if not GOOGLE_API_KEY:
            raise ComponentError(
                "Google API Key is missing", code=404
            )
        return True

    async def find_place(
        self,
        address: str,
        place_prefix: str = None,
        fields="place_id,plus_code"
    ) -> tuple:
        """Searches for a place using the Google Places API.

        Args:
            idx: row index
            row: pandas row
            return_pluscode: return the Google +Code
            place_prefix: adding a prefix to address

        Returns:
            The Place ID of the first matching result, or None if no results are found.
        """
        base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        async with self.semaphore:  # Use the semaphore to limit concurrent requests
            params = {
                "input": address,
                "inputtype": "textquery",
                "fields": fields,
                "key": GOOGLE_API_KEY
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params) as response:
                    if response.status == 200:
                        result = await response.json()
                        if result['status'] == 'OK' and result["candidates"]:
                            candidate = result["candidates"][0]
                            place_id = candidate["place_id"]
                            plus_code = candidate['plus_code'].get('compound_code')
                            global_code = candidate['plus_code'].get('global_code')
                            return place_id, plus_code, global_code
            return None, None, None

    async def get_coordinates(
        self,
        idx,
        row,
        return_pluscode: bool = False,
        place_prefix: str = None
    ):
        async with self.semaphore:  # Use the semaphore to limit concurrent requests
            street_address = self.columns[0]
            if pd.notnull(row[street_address]):
                try:
                    address = ', '.join(
                        [
                            str(row[column]) for column in self.columns if column is not None
                        ]
                    )
                except TypeError:
                    address = row[street_address]
                if not address:
                    return idx, None
                if place_prefix:
                    try:
                        place_prefix = row[place_prefix]
                    except (ValueError, KeyError):
                        pass
                    address = f"{place_prefix} {address}"
                self._logger.notice(
                    f"Looking for {address}"
                )
                more_params = {}
                if hasattr(self, 'keywords'):
                    keywords = []
                    for element in self.keywords:
                        keywords.append(f"keyword:{element}")
                    more_params = {
                        "components": "|".join(keywords)
                    }
                params = {
                    "address": address,
                    **more_params,
                    "key": GOOGLE_API_KEY
                }
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(self.base_url, params=params) as response:
                            if response.status == 200:
                                result = await response.json()
                                if result['status'] == 'OK':
                                    data = result['results'][0]
                                    more_args = {}
                                    plus_code = None
                                    global_code = None
                                    # Check if it's a subpremise or has an empty plus_code
                                    if "subpremise" in data["types"] or not data.get("plus_code", {}).get("global_code"):
                                        # Refine the search:
                                        place_id, plus_code, global_code = await self.find_place(
                                            address, place_prefix
                                        )
                                    else:
                                        place_id = data['place_id']
                                        try:
                                            plus_code = data['plus_code'].get('compound_code')
                                            global_code = data['plus_code'].get('global_code')
                                        except KeyError:
                                            pass
                                    # extract all information:
                                    if return_pluscode is True:
                                        more_args = {
                                            "plus_code": plus_code,
                                            "global_code": global_code
                                        }
                                    # Extract postal code
                                    postal_code = None
                                    for component in data['address_components']:
                                        if 'postal_code' in component['types']:
                                            postal_code = component['long_name']
                                            break
                                    latitude = data['geometry']['location']['lat']
                                    longitude = data['geometry']['location']['lng']
                                    formatted_address = data['formatted_address']
                                    return idx, {
                                        "latitude": latitude,
                                        "longitude": longitude,
                                        "formatted_address": formatted_address,
                                        "place_id": place_id,
                                        "zipcode": postal_code,
                                        **more_args
                                    }
                except asyncio.TimeoutError as exc:
                    self._logger.error(
                        f"TimeoutException: {exc}"
                    )
                    return idx, None
                except TypeError as exc:
                    self._logger.error(
                        f"TypeError: {exc}"
                    )
                    return idx, None
            return idx, None

    def column_exists(self, column: str):
        if column not in self.data.columns:
            self._logger.warning(
                f"Column {column} does not exist in the dataframe"
            )
            self.data[column] = None
            return False
        return True

    async def run(self):
        # initialize columns:
        self.column_exists('place_id')
        self.column_exists('latitude')
        self.column_exists('longitude')
        self.column_exists('formatted_address')
        self.column_exists('zipcode')

        tasks = [
            self.get_coordinates(
                idx,
                row,
                return_pluscode=self.return_pluscode,
                place_prefix=self.place_prefix
            ) for idx, row in self.data.iterrows()
            if pd.isnull(row[self.check_field])
        ]
        results = await asyncio.gather(*tasks)
        for idx, result in results:
            self._counter += 1
            if result:
                for key, value in result.items():
                    self.data.at[idx, key] = value
        self.add_metric("DOWNLOADED", self._counter)
        # if self._debug is True:
        print(self.data)
        print("::: Printing Column Information === ")
        for column, t in self.data.dtypes.items():
            print(column, "->", t, "->", self.data[column].iloc[0])
        self._result = self.data
        return self._result

    async def close(self):
        pass
