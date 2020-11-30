import anontech_vizivault

vault = anontech_vizivault.ViziVault(base_url='localhost:8083', api_key='12345')

result = vault.findByUser(entity_id=265271)

result


result = vault.search(SearchRequest("",""))
