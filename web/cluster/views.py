from django.views.generic import TemplateView, View
from django.http import JsonResponse

from elasticsearch import Elasticsearch
from elasticsearch.client.utils import _make_path


es = Elasticsearch()


class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        keywords = request.GET['keywords'] if request.GET else 'amsterdam'
        keywords = keywords.split(' ')

        request = {
            'query': {
                'terms': {
                    'text': keywords
                }
            },
            'size': 10,
            'sort': {
                "created_at": {
                    "order": "desc"
                }
            },
            'aggs': {
                'authors': {
                    'terms': {
                        'field': 'user.screen_name',
                        'size': 10
                    }
                },
                'keywords': {
                    'significant_terms': {
                        'field': 'text',
                        'size': 10,
                        'jlh': {}
                    }
                },
                'hashtags': {
                    'terms': {
                        'field': 'entities.hashtags.text',
                        'size': 10
                    }
                },
                'urls': {
                    'terms': {
                        'field': 'entities.urls.expanded_url',
                        'size': 10
                    }
                },
                'mentions': {
                    'terms': {
                        'field': 'entities.user_mentions.screen_name',
                        'size': 10
                    }
                }
            }
        }

        result = es.search(body=request)

        context = dict(
            keywords=' '.join(keywords),

            total=result['hits']['total'],
            postings=[dict(author=p['_source']['user']['screen_name'], created_at=p['_source']['created_at'], text=p['_source']['text']) for p in result['hits']['hits']],

            authors=result['aggregations']['authors']['buckets'],
            terms=result['aggregations']['keywords']['buckets'],
            hashtags=result['aggregations']['hashtags']['buckets'],
            urls=result['aggregations']['urls']['buckets'],
            mentions=result['aggregations']['mentions']['buckets'],
        )

        return self.render_to_response(context)


class ClusterView(TemplateView):
    template_name = "cluster.html"

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
                 },
                 'authors': {
                     'terms': {
                         'field': 'user.screen_name',
                         'size': 3
                     }
                 },

             }
        }
        result = es.search(body=request)

        kw = result['aggregations']['topics']['buckets']
        authors = result['aggregations']['authors']['buckets']

        return kw, authors

    def get(self, request, *args, **kwargs):
        keywords = request.GET['keywords'] if request.GET else 'amsterdam'
        keywords = keywords.split(' ')

        data = self._determine_clusters(keywords)

        for cluster in data['clusters']:
            kw, auth = self._cluster_info(cluster, keywords)
            cluster['keywords'] = kw
            cluster['authors'] = auth

        context = dict(
            clusters=data['clusters'],
            keywords=' '.join(keywords)
        )

        return self.render_to_response(context)


class PostingsView(TemplateView):
    template_name = "postings.html"

    def _postings(self, keywords):
        request = {
            'query': {
                'terms': {
                    'text': keywords
                }
             },
             'size': 10
        }
        result = es.search(body=request)

        return result['hits']

    def get(self, request, *args, **kwargs):
        keywords = request.GET['keywords'] if request.GET else 'amsterdam'
        keywords = keywords.split(' ')

        data = self._postings(keywords)

        context = dict(
            total=data['total'],
            postings=[dict(author=p['_source']['user']['screen_name'], created_at=p['_source']['created_at'], text=p['_source']['text']) for p in data['hits']],
            keywords=' '.join(keywords)
        )

        return self.render_to_response(context)


class VolumeView(TemplateView):
    template_name = "volume.html"


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