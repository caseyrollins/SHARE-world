import json
import requests


# GEOCODING_API_KEY = <API_KEY_HERE>


def main():

    page_size = 100

    # determine number of results from SHARE 
    res = requests.get('https://share.osf.io/api/v2/search/entity/_search')
    num_results = res.json()['hits']['total']

    # determine number of requests necessary to retrieve all results
    num_requests = num_results / page_size

    entity_names = []
    # in theory, range(1, num_results), but since the geocoding API only allows 2500 requests/hour, range(1, 25)
    for i in range(1, 25):
        print('requesting page {} / {} from SHARE'.format(i, num_requests-1))
        res = requests.get('https://share.osf.io/api/v2/search/entity/_search?page={}&size={}'.format(i, page_size))
        hits = res.json()['hits']['hits']
        for hit in hits:
            entity_names.append(hit['_source']['name'])

    entity_locations = []
    for index, address in enumerate(entity_names):
        if index == 2500:
            break
        try:
            geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'.format(address, GEOCODING_API_KEY)
        except UnicodeEncodeError:
            continue
        print('requesting address for entity {} / {}'.format(index, len(entity_names)))
        res = requests.get(geocoding_url)
        results = res.json()['results']
        print(results)
        if results:
            location = results[0]['geometry']['location']
            entity_locations.append(location)

    with open('locations.json', 'w') as outfile:
        json.dump(entity_locations, outfile)

if __name__ == '__main__':
    main()
