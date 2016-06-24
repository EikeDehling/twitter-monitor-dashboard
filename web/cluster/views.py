from django.views.generic import TemplateView, View
from django.http import JsonResponse

from elasticsearch import Elasticsearch
from elasticsearch.client.utils import _make_path


es = Elasticsearch()


class IndexView(TemplateView):
    template_name = "index.html"


class VolumeDataView(View):
    def get(self, request, *args, **kwargs):
        keywords = request.GET['keywords'] if request.GET else 'amsterdam'
        keywords = keywords.split(' ')

        request = {
            'query': {
                'bool': {
                    'must': [
                        {
                            'terms': {
                                'text': keywords
                            }
                        },
                        {
                            'range': {
                                'created_at': {
                                    'from': "now-2d/d"
                                }
                            }
                        }
                    ]
                }
            },
            'size': 0,
            'aggs': {
                'volume': {
                    'date_histogram': {
                        'field': 'created_at',
                        'interval': '15m',
                        'format': 'yyyy-MM-dd HH:mm'
                    }
                }
            }
        }
        result = es.search(body=request)

        volumes = [{'x': bucket['key'], 'y': bucket['doc_count']}
                   for bucket in result['aggregations']['volume']['buckets']]

        data = [{
            'name': 'Volume',
            'values': volumes
        }]

        return JsonResponse(data, safe=False)


class TagcloudDataView(View):
    def get(self, request, *args, **kwargs):
        keywords = request.GET['keywords'] if request.GET else 'amsterdam'
        keywords = keywords.split(' ')

        request = {
            'query': {
                'terms': {
                    'text': keywords
                }
             },
             'size': 0,
             'aggs': {
                 'terms': {
                     'significant_terms': {
                         'field': 'text',
                         'size': 10,
                         'jlh': {}
                     }
                 }
             }
        }
        result = es.search(body=request)

        data = [{'value': x['key'], 'count': x['doc_count']} for x in result['aggregations']['terms']['buckets']]

        return JsonResponse(data, safe=False)


class TermsDataView(View):

    field = None

    def get(self, request, *args, **kwargs):
        keywords = request.GET['keywords'] if request.GET else 'amsterdam'
        keywords = keywords.split(' ')

        request = {
            'query': {
                'terms': {
                    'text': keywords
                }
             },
             'size': 0,
             'aggs': {
                 'terms': {
                     'terms': {
                         'field': self.field,
                         'size': 10
                     }
                 }
             }
        }
        result = es.search(body=request)

        return JsonResponse(result['aggregations']['terms']['buckets'], safe=False)


class PostingsDataView(View):
    def get(self, request, *args, **kwargs):
        keywords = request.GET['keywords'] if request.GET else 'amsterdam'
        keywords = keywords.split(' ')

        request = {
            'query': {
                'terms': {
                    'text': keywords
                }
             },
             'size': 10
        }
        result = es.search(body=request)

        return JsonResponse([dict(author=p['_source']['user']['screen_name'], created_at=p['_source']['created_at'], text=p['_source']['text']) for p in result['hits']['hits']], safe=False)


class ClusterDataView(View):
    def _determine_clusters(self, keywords):
        request = {
            "search_request": {
                "query": {
                    "terms": {
                        "text": keywords
                    }
                },
                "size": 10000
            },
            "query_hint": ' '.join(keywords),
            "max_hits": 0,
            "field_mapping": {
                "content": ["_source.text"]
            },
            "algorithm": "lingo",
            "attributes": {
                "LingoClusteringAlgorithm.desiredClusterCountBase": 7,
                "LingoClusteringAlgorithm.clusterMergingThreshold": 0.15,
                "TermDocumentMatrixBuilder.maxWordDf": 0.05,
                "DocumentAssigner.minClusterSize": 20
            }
        }
        _, data = es.transport.perform_request('POST', _make_path('twitter', 'tweet', '_search_with_clusters'),
                                               params=dict(request_timeout=120), body=request)
        return data

    def _cluster_info(self, cluster, keywords):
        request = {
            'query': {
                'ids': {
                    'values': cluster['documents']
                 }
             },
             'size': 0,
             'aggs': {
                 'topics': {
                     'significant_terms': {
                         'field': 'text',
                         'size': 10,
                         'jlh': {},
                         "background_filter": {
                             'terms': {
                                 'text': keywords
                             }
                         }
                     }
                 }
             }
        }
        result = es.search(body=request)

        return result['aggregations']['topics']['buckets']

    def get(self, request, *args, **kwargs):
        keywords = request.GET['keywords'] if request.GET else 'amsterdam'
        keywords = keywords.split(' ')

        data = self._determine_clusters(keywords)

        for cluster in data['clusters']:
            cluster['keywords'] = self._cluster_info(cluster, keywords)
            cluster['documents'] = len(cluster['documents'])

        return JsonResponse(data['clusters'], safe=False)