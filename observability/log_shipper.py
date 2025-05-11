import time
import json
from elasticsearch import Elasticsearch

ES_URL = 'http://localhost:9200'
INDEX = 'incident-logs'

es = Elasticsearch(ES_URL)

def ship_log(message: str, level: str = 'INFO'):
    doc = {
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'level': level,
        'message': message
    }
    es.index(index=INDEX, document=doc)

if __name__ == '__main__':
    # Example usage
    ship_log('Incident framework log shipper started', 'INFO') 