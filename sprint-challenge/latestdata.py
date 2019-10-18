from openaq import OpenAQ


def countrycodata(countryname):
    """"Getting the Carbon Monoxid levels of city by Country """
    api = OpenAQ()
    _, body = api.measurements(country=countryname, parameter='co')
    bulk = []
    for result in body['results']:
        city = result['city']
        covalue = result['value']
        
        record = [city,covalue]
        #print(record)
        bulk.append(record)
    return bulk
