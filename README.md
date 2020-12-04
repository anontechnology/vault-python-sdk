## Anontech Python ViziVault Bindings

### Project Description
Anontech vizivault is designed to make the retrieval and storage of personal and sensitive information easy. Our multi-layer encryption/decryption layer will make your data secure and accesable only to memebrs of your organization on a "need-to-use" basis. Data providers, individuals, end users, and even developers can rest safe knownign their personal data is stored securely, access is monitored, and thier most personal data is kept securely seperate from day to day business operations. Personal data is there when you need it most to support business operations and disapers back into the vault when it's not needed. Safe and secure.


### Support
Please report bugs and issues to support@anontech.io

### Requirements
Only `Python 3` is currently supported.

The basic third party dependencies are the requests and pytest. Libraries installation happens automatically during setup.

### Installaion
```
pip install -e git://github.com/anontechnology/vault-python-sdk.git/#egg=vizivault
```

### Importing the Module
```
import vizivault
```

Alternatively you can just take the vault class

```
from vizivault import ViziVault
```

### Authentication
You must provide an application identifier or api key for all operations to identify you and your application to the vault for authenticaion. For data insertion you need to provide a valid encryption key. For data retrieval you need to apply a valid decryption key.

We recommend at a minimum putting your encryption and decryption key locally in a secure location and refer to it with a filehandle.

### Quick start

#### Attaching to your Vault

```
with open('./my_secure_file/test_encryption_key.txt', 'r') as encryption_file:
    encryption_key = encryption_file.read()
with open('./my_secure_file/test_decryption_key.txt', 'r') as decryption_file:
vault = vizivault.ViziVault(base_url='http://localhost:8083', api_key='12345', encryption_key=encryption_key,
                  decryption_key=decryption_key)`
```

#### Attributes

Attributes are how the ViziVault ecosystem organizes your data. Every data point consists of three main components: a user id, which represents who the data is about; a value, which is some piece of information about the user; and an attribute, which expresses the relationship between the user and the value. For example, in an online retail application, there would be an attribute for shipping addresses, an attribute for billing addresses, and an attribute for credit card information.

#### Adding an Attribute to an Entity or User

Attributes are stored as key/value pairs of strings. Both Users and Entities can have Attributes set to them. If there is an existing Attribute in the system with the key of the provided Attribute, that Attribute will be updated; otherwise, a new Attribute will be created.

```
// Retrieving all attributes for a user
new_user = User("exampleUser")
new_user.add_attribute(attribute="FIRST_NAME", value="Jane")
vault.save(new_user)

// Adding an Attribute to entity
entity = vault.find_by_entity("exampleClient")
entity.add_attribute(attribute="FULL_ADDRESS", value="1 Hacker Way, Beverly Hills, CA 90210")
vault.save(entity)
```



### Retrieving all Attributes of an Entity or User
Retrieves all Attributes for the specified entity or user. Returns a list of Attribute objects

```
# Retrieving all attributes for a user
user = vault.find_by_user("User1234")
attributes = user.get_attributes()

# Retrieving all attributes for an entity
entity = vault.find_by_entity("Client6789")
attributes = entity.get_attributes
````

### Searching

To search a Vault for Attributes, pass in a SearchRequest. A list of matching Attributes will be returned. For more information, read about ViziVault search.

```
attributes = vault.search(SearchRequest("LAST_NAME", "Doe"))
```

### Deleting User Attributes
```
// Purging all user attributes
User user = vault.find_by_user("User1234");
vault.purge(user);

// Removing specific attribute
User user = vault.find_by_user("User1234");
user.clear_attribute("LAST_NAME");
vault.save(user);
```

