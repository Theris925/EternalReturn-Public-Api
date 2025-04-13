import requests
import logging
from typing import Final

class ErbsApiClient(object):
    __endpoint:Final[str] = 'https://open-api.bser.io'
    
    @property
    def __HEADER(self) -> dict:
        return {
            'accept': 'application/json',
            'x-api-key': self.__api_key,
        }

    def get_user_num(self, nickname:str) -> str | int:
        """
        Get player number using in-game nickname.

        Args:
            nickname (str):             Player's in-game nickname.
        Returns:
            num (int):                  Player's number.
        """

        user_data:dict = self.__fetch_data('user/nickname/', {('query', nickname),})
        return user_data.get('userNum', '')
    
    def get_user_stats(self, user_data:str|int, seasonId:str|int) -> dict:
        """
        Get player's stats in selected season.

        Args:
            user_data (str, int):       Player's in-game nickname / player's number 
            seasonId (str, int):        Season ID
        Returns:
            stats (dict):               Player's stats.
        """
        return self.__fetch_data(f'user/stats/{self.__format_user_data(user_data)}/{seasonId}')
    
    def get_user_games(self, user_data:str|int) -> dict:
        """
        Get player's recent games.

        Args:
            user_data (str, int):       Player's in-game nickname / player's number
        Returns:
            games (dict):               Player's recent games (~90 days).
        """
        
        return self.__fetch_data(f'user/games/{self.__format_user_data(user_data)}')

    def get_game_details(self, gameId:str|int) -> dict:
        """
        Get details of selected game.

        Args:
            gameId (str, int):          Game ID, which you can get in match history in game.
        Returns:
            game details (dict):        Statistics of selected game.
        """
        return self.__fetch_data(f'games/{gameId}')
    
    def get_metadata(self, metaType:str = 'hash') -> dict:
        """
        Get meta data from selected meta type. Uses version 2 due to the version 1 deprecated.

        Args:
            metaType (str):             Meta type, which you can get using get_metadata_hash().
        Returns:
            meta data (dict):           Meta data.
        """
        
        return self.__fetch_data(f'data/{metaType}', {}, 'v2')

    def get_free_characters(self, matchingMode) -> list:
        """
        Get list of free characters in selected matching mode.

        Args:
            matchingMode (str, int):    Index of matching mode.
        Returns:
            characters (list):          Indices of free characters in selected matching mode.
        """

        return self.__fetch_data(f"freeCharacters/{matchingMode}")
    
    def get_current_season(self) -> int:
        """
        Get current season ID.

        Returns:
            seasonID (int):                 Current season ID.
        """

        for seasonDict in self.get_metadata("Season"):
            if seasonDict['isCurrent'] == 1:
                return seasonDict['seasonID'] - 1

    def get_ranked_top(self, seasonId, matchingTeamMode) -> dict:
        """
        Get top in Ranked.

        Args:
            seasonId (str, int):            ID of season.
            matchingTeamMode (str, int):    Index of matching mode.
        Returns:
            top (dict):                     Top players in selected matching mode and season.
        """

        return self.__fetch_data(f"rank/top/{seasonId}/{matchingTeamMode}")
    
    def get_user_ranked_top(self, user_data, seasonId, matchingTeamMode) -> dict:
        """
        Get user top in Ranked mode.

        Args:
            user_data (str, int):           Player's in-game nickname / player's number
            seasonId (str, int):            ID of season.
            matchingTeamMode (str, int):    Index of matching mode.
        Returns:
            top (dict):                     Top players in selected matching mode and season.
        """

        return self.__fetch_data(f"rank/{self.__format_user_data(user_data)}/{seasonId}/{matchingTeamMode}")

    def get_recommended_routes(self) -> str | int:
        """
        Get recommended route.

        Returns:
            route (int, str):               ID of recommended route.
        """

        return self.__fetch_data(f"weaponRoutes/recommend")
    
    def get_current_route(self, routeId) -> str | int:
        """
        Get current route data.

        Args:
            routeId (str, int):             ID of selected route.
        Returns:
            route data (dict):              Data of current route.
        """

        return self.__fetch_data(f"weaponRoutes/recommend/{routeId}")
    
    def get_language_data(self, language:str="Korean") -> str:
        """
        Get link to current language txt file.

        Args:
            language (str):                 Current language. Ex: Korean
        Returns:
            link (str):                     Language txt file link.
        """

        return self.__fetch_data(f"l10n/{language}")
    
    def __fetch_data(self, url, request_params={}, version=None):
        if version is None: 
            version = self._version

        currentUrl = f'{self.__endpoint}/{version}/{url}'
        
        response:requests.Response = requests.get(currentUrl, headers=self.__HEADER, params=request_params)
        resJson:dict = response.json()

        # response.status_code can return wrong code
        status_code:int = int(resJson['code']) if response.status_code == 200 else response.status_code

        match status_code:
            case 200: logging.info("Success")
            case 400: logging.error("Access denied")
            case 404: logging.warning("This param does not exist")
        
        if resJson['message'] == "Missing Authentication Token":
            return self.__fetch_data(url, request_params, 'v2' if version == 'v1' else 'v1')
        else:
            return resJson[list(resJson.keys())[-1]]
    
    def __format_user_data(self, user_data):
        try:
            return int(user_data)
        except:
            return self.get_user_num(user_data)
    
    def __init__(self, api_key):
        self.__api_key:Final[str] = api_key
        self._version:str = 'v1' #changeable because current version may be deprecated