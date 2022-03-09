from flask import request, redirect, url_for, render_template, flash, session
from application import app
from elasticsearch import Elasticsearch

@app.route('/', methods=['GET', 'POST'])
def show_results():
    """
    TLS通信を無効化することでElasticsearchと通信できているが
    いずれはTLS通信を有効化したい
    参考記事：
    https://discuss.elastic.co/t/elastic-search-connection-error/261348/4#:~:text=Jan%202021-,The%20connection%20to%20the%20elastic%20search%20server%20is%20sucessfully,-l%20but%20I
    """
    es = Elasticsearch(
        "https://elastic:WDvp4jpH3zqRj7T@localhost:9200/",
        #  use_ssl = False,
        ca_certs=False,
        verify_certs=False
        )


    body = {
        "query" : {
            "bool": {
                "must": [
                ]           
            }
        },
        "highlight": {
            "fields": {
                "itemCaption": {}
            }
        }
    }

    if request.form.get('search_word'):
        body['query']['bool']['must'].append(
            {
                "bool": {
                    "should": [
                        { "match": { "title": request.form.get('search_word') } },
                        { "match": { "itemCaption": request.form.get('search_word') } }
                    ]
                }
            }
        )

    if request.form.get('price_min'):
        body['query']['bool']['must'].append({ "range": { "itemPrice": { "gte": request.form.get('price_min') } } })

    if request.form.get('price_max'):
        body['query']['bool']['must'].append({ "range": { "itemPrice": { "lte": request.form.get('price_max') } } })

    result = es.search(index='book', body=body, size=1000)
    result_num = result['hits']['total']['value']
    books = result['hits']['hits']

    return render_template('index.html', result_num=result_num, books=books, request_form=request.form)