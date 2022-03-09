import json
from elasticsearch import Elasticsearch

with open('rakuten_books.json', 'r') as f:
  rakuten_books = json.load(f)

es = Elasticsearch(
  "https://elastic:WDvp4jpH3zqRj7T@localhost:9200/",
#  use_ssl = False,
  ca_certs=False,
  verify_certs=False
  )

#  http_auth=("elastic","WDvp4jpH3zqRj7T")
#  )

for rakuten_book in rakuten_books:
  rakuten_book_item = rakuten_book['Item']
  try:
    es.create(
      index='book',
      id=rakuten_book_item['isbn'],
      document=rakuten_book_item
      )
  except:
    pass
  print('{} created'.format(rakuten_book_item['title']))