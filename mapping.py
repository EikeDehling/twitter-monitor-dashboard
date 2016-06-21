#!./bin/python
from elasticsearch import Elasticsearch

es = Elasticsearch()


def string_unanalyzed():
    return {
        "type": "string",
        "index": "not_analyzed",
        "doc_values": True
    }


def string_analyzed():
    return {
        "type": "string"
    }


def generic(type=None):
    return {
        "type": type,
        "doc_values": True
    }


def date():
    return {
        "type": 'date',
        "doc_values": True,
        "format": "EEE MMM dd HH:mm:ss Z YYYY",
        }


def media():
    return {
        "properties": {
            "w": generic('long'),
            "resize": string_unanalyzed(),
            "h": generic('long')
        }
    }


mapping = {
    "properties": {
        "filter_level":string_unanalyzed(),
        "retweeted": generic('boolean'),
        "in_reply_to_screen_name": string_unanalyzed(),
        "possibly_sensitive": generic('boolean'),
        "truncated": generic('boolean'),
        "lang": string_unanalyzed(),
        "in_reply_to_status_id_str": string_unanalyzed(),
        "id": generic('long'),
        "withheld_in_countries": string_unanalyzed(),
        "scopes": {
            "properties": {
                "place_ids": string_unanalyzed()
            }
        },
        "entities": {
            "properties": {
                "urls": {
                    "properties": {
                        "expanded_url": string_unanalyzed(),
                        "indices": generic('long'),
                        "display_url": string_unanalyzed(),
                        "url":string_unanalyzed()
                    }
                },
                "hashtags": {
                    "properties": {
                        "text": string_unanalyzed(),
                        "indices": generic('long')
                    }
                },
                "media": {
                    "properties": {
                        "sizes": {
                            "properties": {
                                "thumb": media(),
                                "small": media(),
                                "medium": media(),
                                "large": media(),
                                }
                        },
                        "source_user_id": generic('long'),
                        "media_url": string_unanalyzed(),
                        "type": string_unanalyzed(),
                        "display_url": string_unanalyzed(),
                        "url": string_unanalyzed(),
                        "id": generic('long'),
                        "media_url_https": string_unanalyzed(),
                        "video_info": {
                            "properties": {
                                "duration_millis": generic('long'),
                                "variants": {
                                    "properties": {
                                        "bitrate": generic('long'),
                                        "content_type": string_unanalyzed(),
                                        "url": string_unanalyzed()
                                    }
                                },
                                "aspect_ratio": generic('long')
                            }
                        },
                        "expanded_url": string_unanalyzed(),
                        "indices": generic('long'),
                        "source_status_id_str": string_unanalyzed(),
                        "source_user_id_str": string_unanalyzed(),
                        "source_status_id": generic('long'),
                        "id_str": string_unanalyzed()
                    }
                },
                "user_mentions": {
                    "properties": {
                        "id": generic('long'),
                        "name": string_analyzed(),
                        "indices": generic('long'),
                        "screen_name": string_analyzed(),
                        "id_str": string_unanalyzed()
                    }
                }
            }
        },
        "extended_entities": {
            "properties": {
                "media": {
                    "properties": {
                        "sizes": {
                            "properties": {
                                "thumb": media(),
                                "small": media(),
                                "medium": media(),
                                "large": media(),
                                }
                        },
                        "source_user_id": generic('long'),
                        "media_url": string_unanalyzed(),
                        "type": string_unanalyzed(),
                        "display_url": string_unanalyzed(),
                        "url": string_unanalyzed(),
                        "id": generic('long'),
                        "media_url_https": string_unanalyzed(),
                        "video_info": {
                            "properties": {
                                "duration_millis": generic('long'),
                                "variants": {
                                    "properties": {
                                        "bitrate": generic('long'),
                                        "content_type": string_unanalyzed(),
                                        "url": string_unanalyzed()
                                    }
                                },
                                "aspect_ratio": generic('long')
                            }
                        },
                        "expanded_url": string_unanalyzed(),
                        "indices": generic('long'),
                        "source_status_id_str": string_unanalyzed(),
                        "source_user_id_str": string_unanalyzed(),
                        "source_status_id": generic('long'),
                        "id_str": string_unanalyzed()
                    }
                }
            }
        },
        "in_reply_to_user_id_str": string_unanalyzed(),
        "timestamp_ms": string_unanalyzed(),
        "in_reply_to_status_id": generic('long'),
        "created_at": date(),
        "favorite_count": generic('long'),
        "place": {
            "properties": {
                "id": string_unanalyzed(),
                "place_type": string_unanalyzed(),
                "bounding_box": {
                    "properties": {
                        "type": string_unanalyzed(),
                        "coordinates": generic('double')
                    }
                },
                "name": string_analyzed(),
                "attributes": {
                    "type": "object"
                },
                "country_code": string_unanalyzed(),
                "url": string_unanalyzed(),
                "full_name": string_analyzed(),
                "country": string_analyzed()
            }
        },
        "coordinates": {
            "properties": {
                "type": string_unanalyzed(),
                "coordinates": generic('double')
            }
        },
        "text": string_analyzed(),
        "is_quote_status": generic('boolean'),
        "quoted_status_id": generic('long'),
        "source": string_unanalyzed(),
        "favorited": generic('boolean'),
        "retweet_count": generic('long'),
        "in_reply_to_user_id": generic('long'),
        "id_str": string_unanalyzed(),
        "user": {
            "properties": {
                "location":string_unanalyzed(),
                "default_profile": generic('boolean'),
                "statuses_count": generic('long'),
                "profile_background_tile": generic('boolean'),
                "lang": string_unanalyzed(),
                "profile_link_color": string_unanalyzed(),
                "profile_banner_url": string_unanalyzed(),
                "id": generic('long'),
                "protected": generic('boolean'),
                "favourites_count": generic('long'),
                "profile_text_color": string_unanalyzed(),
                "verified": generic('boolean'),
                "description": string_analyzed(),
                "contributors_enabled": generic('boolean'),
                "profile_sidebar_border_color": string_unanalyzed(),
                "name": string_analyzed(),
                "profile_background_color": string_unanalyzed(),
                "created_at": date(),
                "default_profile_image": generic('boolean'),
                "followers_count": generic('long'),
                "geo_enabled": generic('boolean'),
                "profile_image_url_https": string_unanalyzed(),
                "profile_background_image_url": string_unanalyzed(),
                "profile_background_image_url_https": string_unanalyzed(),
                "url": string_unanalyzed(),
                "utc_offset": generic('long'),
                "time_zone": string_unanalyzed(),
                "profile_use_background_image": generic('boolean'),
                "friends_count": generic('long'),
                "profile_sidebar_fill_color": string_unanalyzed(),
                "screen_name": string_unanalyzed(),
                "id_str": string_unanalyzed(),
                "profile_image_url": string_unanalyzed(),
                "is_translator": generic('boolean'),
                "listed_count": generic('long')
            }
        }
    }
}

es.indices.create(index='twitter', body={"number_of_shards": 1, "number_of_replicas": 0, "refresh_interval": "30s"})
es.indices.put_mapping(index='twitter', doc_type='tweet', body=mapping)
