import asyncio
import json
import logging
import os

from requests import Session

from app.utils.config import DB_WEBHOOK
from app.utils.tools import json_get_by_id


class Database:
    def __init__(self, url: str, login: str, password: str):
        self.URL = url
        self.session = Session()
        self.session.auth = (login, password)

    def get(self, subject: str, id: int = "") -> dict | list[dict]:
        """
        Get all entities by subject:
        >>> db.get(db.HOLIDAYS)

        Get entity by id:
        >>> db.get(db.HOLIDAYS,data['id'])
        """
        if id or subject in ["actions", "subjects"]:
        url = f"{self.URL}/{subject}/"
            url += f"{id}/"
            response = self.session.get(url)
            if response.status_code == 404:
                return []
            if response.status_code == 403:
                raise PermissionError
            return response.json()
        else:
            result = []
            next = True
            while next:
                response = self.session.get(url)
                if response.status_code == 403:
                    raise PermissionError
                response = response.json()
                if "results" in response.keys():
                    result = result + response["results"]
                else:
                    result = response
                    next = False
                next = bool(response["next"])
                url = response["next"]
            return result

    def add(self, _subject, **data) -> dict:
        """usage examples:
        >>> data = {'name':..}; db.add(subject=db.HOLIDAYS, **data)
        >>> db.add(subject=db.HOLIDAYS,name='..',..)
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
        >>> db.edit_patch(db.HOLIDAYS, id, name = "abc"..)

        or
        >>> data = {name: "abc"..}

        >>> db.edit_patch(db.HOLIDAYS, id, **data)

        """
        url = f"{self.URL}/{subject}/{id}/"
        response = self.session.patch(url, data=data)
        if response.status_code == 403:
            raise PermissionError
        response = response.json()
        return response

    def delete(self, subject, id, raise_error=True) -> dict:
        """Delete entity
        >>> db.delete(db.HOLIDAYS, id)
        """
        url = f"{self.URL}/{subject}/{id}/"
        response = self.session.delete(url)
        if response.status_code == 403 and raise_error:
            raise PermissionError
        return response

    def filter(self, _subject, return_list=False, **conditions) -> list[dict] | dict:
        """usage:
        >>> db.filter(db.HOLIDAYS,phone_number='+77479309084')"""
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
        >>> db.get_page(db.HOLIDAYS, page=2)
        >>> db.get_page(db.HOLIDAYS, page=2, name='abc')
        """
        url = f"{self.URL}/{subject}/?page={page}"
        for key, value in arg.items():
            url += f"&{key}={value}"
        response = self.session.get(url)
        if response.status_code == 403:
            raise PermissionError
        return response.json()


class Data:
    HOLIDAYS = "holidays"
    PROJECTS = "projects"
    RECIPES = "recipes"
    SUBJECTS = [HOLIDAYS, PROJECTS, RECIPES]

    def __init__(self, db: Database) -> None:
        self.__file_path = os.path.join(os.getcwd(), "app", "data", "data.json")
        self.db = db
        if DB_WEBHOOK:
            self._holidays: list = []
            self._recipes: list = []
            self._projects: list = []
            self.get_holidays = lambda: self._holidays
            self.get_recipes = lambda: self._recipes
            self.get_projects = lambda: self._projects
            self.get_holiday = lambda id: json_get_by_id(self._holidays, id)
            self.get_recipe = lambda id: json_get_by_id(self._recipes, id)
            self.get_project = lambda id: json_get_by_id(self._projects, id)
        else:
            self.get_holidays = lambda: db.get(self.HOLIDAYS)
            self.get_recipes = lambda: db.get(self.RECIPES)
            self.get_projects = lambda: db.get(self.PROJECTS)
            self.get_holiday = lambda id: db.get(self.HOLIDAYS, id)
            self.get_recipe = lambda id: db.get(self.RECIPES, id)
            self.get_project = lambda id: db.get(self.PROJECTS, id)

    def __load_data(self) -> None:
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                data: dict = json.load(file)
                self._holidays = data.get("holidays", {})
                self._recipes = data.get("recipes", {})
                self._projects = data.get("projects", {})
                return
        except FileNotFoundError:
            logging.error("⭕Local data is not available, considering empty...⭕")
        except Exception as e:
            logging.error(f"⭕Error while loading data: {e}⭕")
        # code below executes only if (any) exception occured
        self._holidays = {}
        self._recipes = {}
        self._projects = {}

    def __save_data(self) -> None:
        data = {
            "holidays": self._holidays,
            "recipes": self._recipes,
            "projects": self._projects,
        }
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(data, file)

    async def update_async(self, update_subject="", seconds: int = 2):
        """retrieves data from database and saves it to file
        if database is not available and all data is empty, tries to load from file"""
        logging.info("🔵 Retrieving data from database..")

        # This ensures getting new data considering how Database works
        await asyncio.sleep(seconds)

        if update_subject:
            if update_subject in self.SUBJECTS:
                try:
                    data = self.db.get(update_subject)
                except Exception as e:
                    logging.error("⭕Database is not available" + "\n⭕ Error: {e} ⭕")
                setattr(self, "_" + update_subject, data)
            else:
                logging.error(f'⭕Unknown subject "{update_subject}"⭕')
        else:
            try:
                self._holidays = self.db.get(self.HOLIDAYS)
                self._recipes = self.db.get(self.RECIPES)
                self._projects = self.db.get(self.PROJECTS)
            except Exception as e:
                logging.error("⭕Database is not available" + "\n⭕ Error: {e} ⭕")
                if not any((self._holidays, self._recipes, self._projects)):
                    self.__load_data()
        self.__save_data()
