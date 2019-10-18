from openaq import OpenAQ


def sendhomedata():
    """Getting the Los Angeles data of pm25 levels """
    api = OpenAQ()
    _, body = api.measurements(city='Los Angeles', parameter='pm25')
    #getting utcdate time and pmi value from body results
    sendresults = []
    for result in body['results']:
        utcdatetime = result['date']['utc']
        pmivalue = result['value']
        oneresult = (utcdatetime,str(pmivalue))
        sendresults.append(oneresult)
    
    return sendresults
