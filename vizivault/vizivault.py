import requests
import json
import os
from requests import Response
from typing import List

from vizivault.entity import Entity
from vizivault.user import User
from vizivault.vault_response_excption import VaultResponseException
from vizivault.vault_communication_exception import VaultCommunicationException
from vizivault.attribute import Attribute
from vizivault.tag import Tag
from vizivault.regulation import Regulation
from vizivault.search_request import SearchRequest
from vizivault.entity_definition import EntityDefinition
from vizivault.attribute_definition import AttributeDefinition
from vizivault.attribute_set import AttributeSet


class ViziVault:

    def __init__(self, base_url: str, api_key: str, encryption_key: str = None, decryption_key: str = None):
        self.content_type = "application/json"
        self.base_url = base_url
        self.api_key = api_key
        self.encryption_key = encryption_key or os.environ.get('VV_ENCRYPT_KEY', None)
        self.decryption_key = decryption_key or os.environ.get('VV_DECRYPT_KEY', None)

    def __get_with_decryption_key(self, url_suffix) -> Response:
        headers = {"X-Decryption-Key": self.decryption_key}
        return self.__get(url_suffix=url_suffix, headers=headers)

    def __post_with_encryption_key(self, url_suffix, body) -> Response:
        headers = {"X-Encryption-Key": self.encryption_key, "Content-Type": self.content_type}
        return self.__post(url_suffix=url_suffix, body=body, headers=headers)

    def __post(self, url_suffix, body, headers=None) -> Response:
        headers = headers or {"Content-Type": self.content_type, "Authorization": self.api_key}
        try:
            if isinstance(body, str):
                response = requests.post(url=self.base_url + url_suffix, data=body, headers=headers)
            else:
                response = requests.post(url=self.base_url + url_suffix, json=body, headers=headers)

            if not response.ok:
                error_message = "No message provided" if response.content is None else json.loads(response.content)[
                    'message']
                raise VaultResponseException(message=error_message, status=response.status_code)
            return response
        except TypeError:
            pass
        except IOError as e:
            raise VaultCommunicationException from e

    def __get(self, url_suffix, headers=None) -> Response:
        headers = headers or {"Authorization": self.api_key}
        try:
            response = requests.get(url=self.base_url + url_suffix, headers=headers)
            if not response.ok:
                error_message = "No message provided" if response.content is None else json.loads(response.content)[
                    'message']
                raise VaultResponseException(message=error_message, status=response.status_code)

            return response
        except IOError as e:
            raise VaultCommunicationException from e

    def __delete(self, url_suffix) -> bytes:
        try:
            headers = {"Authorization": self.api_key}
            response = requests.delete(url=self.base_url + url_suffix, headers=headers)

            if not response.ok:
                error_message = "No message provided" if response.content is None else json.loads(response.content)[
                    'message']
                raise VaultResponseException(message=error_message, status=response.status_code)

            return response.content
        except IOError as e:
            raise VaultCommunicationException from e

    def find_by_entity(self, entity_id: str) -> Entity:
        """
        Retrieves all attributes for an entity with the specified ID, as well as entity-level metadata.
        :param entity_id: str
        :return: Entity
        """
        data = json.loads(self.__get_with_decryption_key("/entities/%s/attributes" % entity_id).content)['data'],
        return Entity(entity_id=entity_id, data=data)

    def find_by_user(self, entity_id: str) -> User:
        """
        Retrieves all attributes for a user with the specified ID, as well as user-level metadata.
        :param entity_id: str
        :return: User
        """
        data = json.loads(self.__get_with_decryption_key("/users/%s/attributes" % entity_id).content)['data']
        return User(entity_id=entity_id, data=data)

    def save(self, entity: Entity):
        """
        Updates a user or entity to match changes that have been made client-side,
        by deleting or creating attributes in the vault as necessary.

        :param entity: Entity
        """
        if not isinstance(entity, Entity):
            raise TypeError(
                'Argument entity is not of type Entity'
            )
        for attribute in entity.deleted_attributes:
            self.__delete(f"/users/{entity.id}/attributes/{attribute}")
        entity.deleted_attributes.clear()
        entity_definition = json.dumps(EntityDefinition(entity), default=lambda o: o.__dict__)
        self.__post("/users" if isinstance(entity, User) else "/entities", entity_definition)
        storage_request = AttributeSet(entity.changed_attributes).to_json()
        self.__post_with_encryption_key(f"/users/{entity.id}/attributes", storage_request)
        entity.changed_attributes.clear()

    def purge(self, entity: Entity):
        """
        Deletes all attributes of a user/entity
        :param entity: Entity
        """
        if not isinstance(entity, Entity):
            raise TypeError(
                'Argument entity is not of type Entity'
            )

        self.__delete(f"/users/{entity.id}/data")
        entity.purge()

    def store_attribute_definition(self, attribute_definition: AttributeDefinition) -> Response:
        """
        Creates or updates an attribute definition.

        :param attribute_definition: AttributeDefinition
        :return: Response (http Response)
        """
        if not isinstance(attribute_definition, AttributeDefinition):
            raise TypeError(
                'Argument attribute_definition is not of type Attribute Definition'
            )
        attribute_definition_json = attribute_definition.to_json()
        result = self.__post("/attributes", attribute_definition_json)
        return result

    def get_attribute_definition(self, attribute_key: str) -> AttributeDefinition:
        """
        Gets an attribute definition with the specified name

        :param attribute_key:
        :return: AttributeDefinition
        """
        attribute_definition = AttributeDefinition.from_json(
            self.__get_with_decryption_key(f"/attributes/{attribute_key}").content)
        return attribute_definition

    def get_attribute_definitions(self) -> List[AttributeDefinition]:
        """
        Lists all attribute definitions in the vault
        :rtype list[AttributeDefinition]
        :return: list of all attribute definition in the vault

        """
        return AttributeDefinition.from_json(self.__get_with_decryption_key(f"/attributes").content)

    def store_tag(self, tag: Tag):
        """
        Creates or updates a tag

        :param tag: Tag
        """
        if not isinstance(tag, Tag):
            raise TypeError(
                'Argument tag is not of type Tag'
            )
        tag_json = tag.to_json()
        self.__post("/tags", tag_json)

    def get_tag(self, name: str) -> Tag:
        """
        Get a Tag
        :param name: primary key for tag
        :return: Tag
        :rtype: Tag
        """
        new_tag = Tag.from_json(self.__get(f'/tags/{name}').content)
        return new_tag

    def get_tags(self) -> List[Tag]:
        """
        List all tags in vault
        :rtype list[Tag[
        :return: list of all lags in vault
        """
        return Tag.from_json(self.__get_with_decryption_key('/tags/').content)

    def delete_tag(self, tag: str) -> bool:
        """
        Deletes a tag. This will remove all tag from the vault

        :rtype: bool
        :param tag: str
        :return: true/false if delete was successful
        """
        try:
            self.__delete(f"/tags/{tag}")
            return True
        except VaultResponseException:
            return False

    def store_regulation(self, regulation: Regulation):
        """
        Creates or updates a regulation
        :param regulation: Regulation object
        """
        if not isinstance(regulation, Regulation):
            raise TypeError('Argument regulation is not of type Regulation')
        json_regulation = regulation.to_json()
        self.__post("/regulations", json_regulation)

    def get_regulations(self) -> List[Regulation]:
        """
        Lists all regulations in the vault

        :rtype: list[Regulations]
        :return: list of all regulations in the vault
        """

        return Regulation.from_json(self.__get_with_decryption_key('/regulations/').content)

    def get_regulation(self, key: str) -> Regulation:
        """
        Get a regulation with the specified key

        :rtype: Regulation
        :param key: primary key value of regulation
        :return: Regulation
        """
        return Regulation.from_json(self.__get_with_decryption_key(f'/regulations/{key}').content)

    def delete_regulation(self, regulation) -> bool:
        """
        Deletes a regulation

        :rtype: bool
        :param regulation: regulation object
        :return: True/False
        """
        try:
            self.__delete(f"/regulations/{regulation}")
            return True
        except VaultResponseException:
            return False

    def search(self, search_request: SearchRequest, page: int, count: int) -> List[Attribute]:
        """

        :rtype: List[Attribute]
        :param search_request: SearchRequest
        :param page: (int) - THe page offset of search results
        :param count: (int) - The number of attributes in a result
        :return: List of attributes found in search
        """
        if not isinstance(search_request, SearchRequest):
            raise TypeError('Argument search_request is not of type SearchRequest')
        paginated_search_request = f'{{"query": {search_request.to_json()}, "page": {page}, "count": {count}}}'
        return Attribute.from_json(self.__post("/search/", paginated_search_request).content)

    def get_data_point(self, data_point_id: str) -> Attribute:
        """

        :rtype: Attribute
        :param data_point_id: (int) attribute primary key
        :return: Attribute associated with the attribute
        """
        return Attribute.from_json(self.__get_with_decryption_key(f"/data/{data_point_id}").content)
