from requests import Session
from app.utils.tools import json_get_by_id
import logging
class Database:
    def __init__(self, url: str, login: str, password: str):
        self.URL = url
        self.session = Session()
        self.session.auth = (login, password)
        self.HOLIDAYS = 'holidays'
        self.PROJECTS = 'projects'
        self.RECIPES = 'recipes'

    def get(self, subject: str, id: int = '') -> dict | list[dict]:
        """
        Get all entities by subject: 
        >>> db.get(db.HOLIDAYS)

        Get entity by id: 
        >>> db.get(db.HOLIDAYS,data['id'])
        """
        url = f'{self.URL}/{subject}'
        if id or subject in ['actions', 'subjects']:
            url += f'/{id}'
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
                if 'results' in response.keys():
                    result = result + response['results']
                else:
                    result = response
                    next = False
                next = bool(response['next'])
                url = response['next']
            return result

    def add(self, _subject, **data) -> dict:
        """usage examples:
        >>> data = {'name':..}; db.add(subject=db.HOLIDAYS, **data)
        >>> db.add(subject=db.HOLIDAYS,name='..',..)
        """
        url = f'{self.URL}/{_subject}/'
        response = self.session.post(url, data=data, allow_redirects=False)

        try:
            response = response.json()
        except:
            pass
        return response

    def edit_put(self, subject, object, **data) -> dict:
        """For operations with ManyToMany, as patch cannot set None for them
        """
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
        url = f'{self.URL}/{subject}/{id}/'
        response = self.session.patch(url, data=data)
        if response.status_code == 403:
            raise PermissionError
        response = response.json()
        return response

    def delete(self, subject, id, raise_error=True) -> dict:
        """ Delete entity
        >>> db.delete(db.HOLIDAYS, id)
        """
        url = f'{self.URL}/{subject}/{id}/'
        response = self.session.delete(url)
        if response.status_code == 403 and raise_error:
            raise PermissionError
        return response

    def filter(self, _subject, return_list=False, **conditions) -> list[dict] | dict:
        """usage:
        >>> db.filter(db.HOLIDAYS,phone_number='+77479309084')"""
        url = f'{self.URL}/{_subject}/?'
        for field, value in conditions.items():
            value = str(value).replace('+', r'%2B')
            url += f'{field}={value}&'
        response = self.session.get(url)
        if response.status_code == 403:
            raise PermissionError
        if 'Select a valid choice' in str(response.json()):
            return []
        result = response.json()['results']
        if len(result) == 1 and not return_list:
            return response.json()['results'][0]
        else:
            return response.json()['results']

    def get_page(self, subject, page='1', **arg):
        """usage:
        >>> db.get_page(db.HOLIDAYS, page=2)
        >>> db.get_page(db.HOLIDAYS, page=2, name='abc')
        """
        url = f'{self.URL}/{subject}/?page={page}'
        for key, value in arg.items():
            url += f'&{key}={value}'
        response = self.session.get(url)
        if response.status_code == 403:
            raise PermissionError
        return response.json()
class Data:
    def __init__(self, db: Database) -> None:
        self.db = db
        try:
            self.holidays = db.get(db.HOLIDAYS)
            self.recipes = db.get(db.RECIPES)
            self.projects = db.get(db.PROJECTS)
        except Exception as e:
            logging.error(e)
            print("Database not available right now")
            self.holidays = {}
            self.recipes = {}
            self.projects = {}
    
    def update(self):
        self.__init__(self.db)
        return self

    async def update_async(self, seconds: int = 2):
        """ update data after getting webhook
            This ensures getting new data considering how Database works"""
        await asyncio.sleep(seconds)
        return self.update()

    def recipe(self, id):
        return json_get_by_id(self.recipes, id)
    
    def holiday(self, id):
        return json_get_by_id(self.holidays, id)
    
    def project(self, id):
        return json_get_by_id(self.projects, id)