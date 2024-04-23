import asyncio
import json
import logging
import os

from requests import Session

from app.utils.config import DB_WEBHOOK
from app.utils.tools import json_get_by_id

HOLIDAYS = "holidays"
PROJECTS = "projects"
RECIPES = "recipes"
SUBJECTS = [HOLIDAYS, PROJECTS, RECIPES]


class Database:
    def __init__(self, url: str, login: str, password: str):
        self.URL = url
        self.session = Session()
        self.session.auth = (login, password)

    def get(self, subject: str, id: int = 0) -> dict | list[dict]:
        """
        Get all entities by subject:
        >>> db.get(HOLIDAYS)

        Get entity by id:
        >>> db.get(HOLIDAYS,data['id'])
        """
        url = f"{self.URL}/{subject}/"
        if id:
            url += f"{id}/"
            response: dict = self.session.get(url)
            if response.status_code == 404:
                return []
            if response.status_code == 403:
                raise PermissionError
            return response.json()
        else:
            result: list[dict] = []
            next = True
            while next:
                response = self.session.get(url)
                if response.status_code == 403:
                    raise PermissionError
                data = response.json()
                if "results" in data.keys():
                    result = result + data["results"]
                else:
                    result = data
                    next = False
                next = bool(data["next"])
                url = data["next"]
            return result

    def add(self, _subject, **data) -> dict:
        """usage examples:
        >>> data = {'name':..}; db.add(subject=HOLIDAYS, **data)
        >>> db.add(subject=HOLIDAYS,name='..',..)
        """
        url = f"{self.URL}/{_subject}/"
        response = self.session.post(url, data=data, allow_redirects=False)

        try:
            response = response.json()
        except:
            pass
        return response

    def edit_put(self, subject, object, **data) -> dict:
        """For operations with ManyToMany, as patch cannot set None for them"""
        for key, value in data.items():
            object[key] = value
        url = f'{self.URL}/{subject}/{object["id"]}/'
        response = self.session.put(url, data=object)
        if response.status_code == 403:
            raise PermissionError
        response = response.json()
        return response

    def edit_patch(self, subject, id, **data) -> dict:
        """For anything except ManyToMany.

        Examples:
        >>> db.edit_patch(HOLIDAYS, id, name = "abc"..)

        or
        >>> data = {name: "abc"..}

        >>> db.edit_patch(HOLIDAYS, id, **data)

        """
        url = f"{self.URL}/{subject}/{id}/"
        response = self.session.patch(url, data=data)
        if response.status_code == 403:
            raise PermissionError
        response = response.json()
        return response

    def delete(self, subject, id, raise_error=True) -> dict:
        """Delete entity
        >>> db.delete(HOLIDAYS, id)
        """
        url = f"{self.URL}/{subject}/{id}/"
        response = self.session.delete(url)
        if response.status_code == 403 and raise_error:
            raise PermissionError
        return response

    def filter(self, _subject, return_list=False, **conditions) -> list[dict] | dict:
        """usage:
        >>> db.filter(HOLIDAYS,phone_number='+49123456789')"""
        url = f"{self.URL}/{_subject}/?"
        for field, value in conditions.items():
            value = str(value).replace("+", r"%2B")
            url += f"{field}={value}&"
        response = self.session.get(url)
        if response.status_code == 403:
            raise PermissionError
        if "Select a valid choice" in str(response.json()):
            return []
        result = response.json()["results"]
        if len(result) == 1 and not return_list:
            return response.json()["results"][0]
        else:
            return response.json()["results"]

    def get_page(self, subject, page="1", **arg):
        """usage:
        >>> db.get_page(HOLIDAYS, page=2)
        >>> db.get_page(HOLIDAYS, page=2, name='abc')
        """
        url = f"{self.URL}/{subject}/?page={page}"
        for key, value in arg.items():
            url += f"&{key}={value}"
        response = self.session.get(url)
        if response.status_code == 403:
            raise PermissionError
        return response.json()


if not DB_WEBHOOK:

    class Data:
        def __init__(self, db: Database) -> None:
            self.get_holidays = lambda: db.get(HOLIDAYS)
            self.get_recipes = lambda: db.get(RECIPES)
            self.get_projects = lambda: db.get(PROJECTS)
            self.get_holiday = lambda id: db.get(HOLIDAYS, int(id))
            self.get_recipe = lambda id: db.get(RECIPES, int(id))
            self.get_project = lambda id: db.get(PROJECTS, int(id))

else:

    class Data:
        __file_path = os.path.join(os.getcwd(), "app", "data", "data.json")
        _holidays: dict = {}
        _recipes: dict = {}
        _projects: dict = {}

        def __init__(self, db: Database) -> None:
            self.db = db

            self.get_holidays = lambda: self._holidays.values()
            self.get_recipes = lambda: self._recipes.values()
            self.get_projects = lambda: self._projects.values()
            self.get_holiday = lambda id: self._holidays[int(id)]
            self.get_recipe = lambda id: self._recipes[int(id)]
            self.get_project = lambda id: self._projects[int(id)]

        def load_from_file(self) -> None:
            logging.info("🔵 Retrieving data from file..")
            try:
                with open(self.__file_path, "r", encoding="utf-8") as file:
                    data: dict = json.load(file)
                    self._holidays = data.get("holidays", {})
                    self._recipes = data.get("recipes", {})
                    self._projects = data.get("projects", {})
                    logging.info("🔵 Data was retrieved from file")
                    return
            except FileNotFoundError:
                logging.error("⭕Local data is not available, considering empty...⭕")
            except Exception as e:
                logging.error(f"⭕Error while loading data: {e}⭕")
            # code below executes only if (any) exception occured
            self._holidays = {}
            self._recipes = {}
            self._projects = {}

        def __save_to_file(self) -> None:
            data = {
                "holidays": self._holidays,
                "recipes": self._recipes,
                "projects": self._projects,
            }
            with open(self.__file_path, "w", encoding="utf-8") as file:
                json.dump(data, file)

        async def update_async(self, update_subject="", seconds: int = 2):
            """retrieves data from database and saves it to file
            if database is not available and all data is empty, tries to load from file
            """
            logging.info("🔵 Retrieving data from database..")

            # This ensures getting new data considering how Database works
            await asyncio.sleep(seconds)

            if update_subject:
                if update_subject in SUBJECTS:
                    try:
                        data = Data.convert_to_dict(self.db.get(update_subject))
                    except Exception as e:
                        logging.error(
                            "⭕Database is not available" + f"\n⭕ Error: {e} ⭕"
                        )
                        return
                    setattr(self, "_" + update_subject, data)
                else:
                    logging.error(f'⭕Unknown subject "{update_subject}"⭕')
            else:
                try:
                    self._holidays = Data.convert_to_dict(self.db.get(HOLIDAYS))
                    self._recipes = Data.convert_to_dict(self.db.get(RECIPES))
                    self._projects = Data.convert_to_dict(self.db.get(PROJECTS))
                except Exception as e:
                    logging.error("⭕Database is not available" + f"\n⭕ Error: {e} ⭕")
                    if not any((self._holidays, self._recipes, self._projects)):
                        self.load_from_file()
                        return
            self.__save_to_file()
            logging.info("🔵 Data was retrieved from database")

        @staticmethod
        def convert_to_dict(_list: list) -> dict:
            """converts list of elements to dict like {id: element}"""
            return {d["id"]: d for d in _list}
