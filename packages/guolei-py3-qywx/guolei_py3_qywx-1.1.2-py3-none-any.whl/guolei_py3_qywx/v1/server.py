#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
=================================================
qywx Server Class Library
-------------------------------------------------
作者：[郭磊]
手机：[15210720528]
Email：[174000902@qq.com]
Github：https://github.com/guolei19850528/guolei_py3_qywx
=================================================
"""
import hashlib
from datetime import timedelta
from types import NoneType
from typing import Union, Callable

import diskcache
import redis
import requests
from addict import Dict
from jsonschema import validate
from jsonschema.validators import Draft202012Validator


class Api(object):
    """
    @see https://developer.work.weixin.qq.com/document/path/90664
    """

    def __init__(
            self,
            base_url: str = "https://qyapi.weixin.qq.com",
            corpid: str = "",
            corpsecret: str = "",
            agentid: Union[int, str] = "",
            diskcache_cache: diskcache.Cache = None,
            redis_cache: Union[redis.Redis, redis.StrictRedis] = None
    ):
        validate(instance=base_url, schema={"type": "string", "minLength": 1, "format": "uri", })
        validate(instance=corpid, schema={"type": "string", "minLength": 1, })
        validate(instance=corpsecret, schema={"type": "string", "minLength": 1, })
        validate(
            instance=agentid,
            schema={
                "oneOf": [{"type": "string", "minLength": 1, }, {"type": "integer", "minimum": 1, }]
            }
        )
        self._base_url = base_url
        self._corpid = corpid
        self._corpsecret = corpsecret
        self._agentid = agentid
        self._diskcache_cache = diskcache_cache
        self._redis_cache = redis_cache
        self._access_token = ""

    @property
    def base_url(self):
        return self._base_url[:-1] if self._base_url.endswith("/") else self._base_url

    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url

    @property
    def corpid(self):
        return self._corpid

    @corpid.setter
    def corpid(self, corpid):
        self._corpid = corpid

    @property
    def corpsecret(self):
        return self._corpsecret

    @corpid.setter
    def corpsecret(self, corpsecret):
        self._corpsecret = corpsecret

    @property
    def agentid(self):
        return self._agentid

    @agentid.setter
    def agentid(self, agentid):
        self._agentid = agentid

    @property
    def diskcache_cache(self):
        return self._diskcache_cache

    @diskcache_cache.setter
    def diskcache_cache(self, diskcache_cache):
        self._diskcache_cache = diskcache_cache

    @property
    def redis_cache(self):
        return self._redis_cache

    @redis_cache.setter
    def redis_cache(self, redis_cache):
        self._redis_cache = redis_cache

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        self._access_token = access_token

    def query_api_domain_ip_list(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        获取企业微信接口IP段

        @see https://developer.work.weixin.qq.com/document/path/92520

        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/cgi-bin/get_api_domain_ip")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", Dict())
        request_func_kwargs.params.setdefault("corpid", self.corpid)
        request_func_kwargs.params.setdefault("corpsecret", self.corpsecret)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "errcode": {"type": "integer", "const": 0},
                            "ip_list": {"type": "array", "minItems": 1},
                            "required": ["errcode", "access_token"],
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).ip_list
        return None

    def query_access_token(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        获取access_token

        @see https://developer.work.weixin.qq.com/document/path/91039

        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/cgi-bin/gettoken")
        request_func_kwargs.setdefault("method", f"GET")
        request_func_kwargs.setdefault("params", Dict())
        request_func_kwargs.params.setdefault("corpid", self.corpid)
        request_func_kwargs.params.setdefault("corpsecret", self.corpsecret)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "errcode": {"type": "integer", "const": 0},
                            "access_token": {"type": "string", "minLength": 1},
                            "required": ["errcode", "access_token"],
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).access_token
        return None

    def access_token_with_diskcache_cache(
            self,
            key: str = None,
            expire: float = timedelta(minutes=110).total_seconds(),
            query_access_token_func_kwargs: dict = {},
    ):
        if not Draft202012Validator({"type": "number"}).is_valid(key):
            expire = timedelta(minutes=110).total_seconds()
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(query_access_token_func_kwargs, dict)):
            query_access_token_func_kwargs = {}
        query_access_token_func_kwargs = Dict(query_access_token_func_kwargs)
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(self.diskcache_cache, diskcache.Cache)):
            if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(key):
                key = "_".join([
                    "guolei_py3_qywx_v1_server_api_diskcache_cache",
                    "access_token",
                    hashlib.md5(
                        f"{self.base_url}_{self.corpid}_{self.corpsecret}_{self.agentid}".encode("utf-8")
                    ).hexdigest()
                ])
            self.access_token = self.diskcache_cache.get(key)
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(self.query_api_domain_ip_list(), NoneType)):
            self.access_token = self.query_access_token(**query_access_token_func_kwargs.to_dict())
            if Draft202012Validator({"type": "string", "minLength": 1}).is_valid(self.access_token):
                self.diskcache_cache.set(
                    key=key,
                    value=self.access_token,
                    expire=expire
                )
        return self

    def access_token_with_redis_cache(
            self,
            key: str = None,
            expire: Union[int, timedelta] = timedelta(minutes=110),
            query_access_token_func_kwargs: dict = {},
    ):
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(query_access_token_func_kwargs, dict)):
            query_access_token_func_kwargs = {}
        query_access_token_func_kwargs = Dict(query_access_token_func_kwargs)
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(self.redis_cache, (redis.Redis, redis.StrictRedis))):
            if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(key):
                key = "_".join([
                    "guolei_py3_qywx_v1_server_api_redis_cache",
                    "access_token",
                    hashlib.md5(
                        f"{self.base_url}_{self.corpid}_{self.corpsecret}_{self.agentid}".encode("utf-8")
                    ).hexdigest()
                ])
            self.access_token = self.redis_cache.get(key)
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(self.query_api_domain_ip_list(), NoneType)):
            self.access_token = self.query_access_token(**query_access_token_func_kwargs.to_dict())
            if Draft202012Validator({"type": "string", "minLength": 1}).is_valid(self.access_token):
                self.redis_cache.setex(
                    name=key,
                    value=self.access_token,
                    time=expire
                )
        return self

    def access_token_with_cache(
            self,
            types: str = None,
            key: str = None,
            expire: Union[float, int, timedelta] = None,
            query_access_token_func_kwargs: dict = {},
    ):
        if not Draft202012Validator({"type": "string", "minLength": 1}).is_valid(types):
            types = "diskcache_cache"
        if types.lower() not in ["diskcache_cache", "redis_cache"]:
            types = "diskcache_cache"
        if types.lower() == "diskcache_cache":
            return self.access_token_with_diskcache_cache(
                key=key,
                expire=expire,
                query_access_token_func_kwargs=query_access_token_func_kwargs
            )
        if types.lower() == "redis_cache":
            return self.access_token_with_redis_cache(
                key=key,
                expire=expire,
                query_access_token_func_kwargs=query_access_token_func_kwargs
            )

        raise ValueError("Cache type must be 'diskcache_cache' or 'redis_cache'")

    def message_send(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        发送应用消息

        @see https://developer.work.weixin.qq.com/document/path/90236

        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/cgi-bin/message/send")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", Dict())
        request_func_kwargs.params.setdefault("access_token", self.access_token)
        request_func_kwargs.setdefault("json", Dict())
        request_func_kwargs.json.setdefault("agentid", self.agentid)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "errcode": {"type": "integer", "const": 0},
                            "required": ["errcode"],
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json())
        return None

    def media_upload(
            self,
            types: str = "file",
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        上传临时素材

        @see https://developer.work.weixin.qq.com/document/path/90253

        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/cgi-bin/media/upload")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", Dict())
        request_func_kwargs.params.setdefault("access_token", self.access_token)
        request_func_kwargs.params.setdefault("type", types)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "errcode": {"type": "integer", "const": 0},
                            "media_id": {"type": "string", "minLength": 1},
                            "required": ["errcode", "media_id"],
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json())
        return None

    def media_uploadimg(
            self,
            request_func_kwargs: dict = {},
            request_func_response_callable: Callable = None
    ):
        """
        上传图片

        @see https://developer.work.weixin.qq.com/document/path/90256

        :param request_func_kwargs: requests.request(**request_func_kwargs)
        :param request_func_response_callable: request_func_response_callable(response, request_func_kwargs)
        :return:
        """
        if not Draft202012Validator({"type": "boolean", "const": True}).is_valid(isinstance(request_func_kwargs, dict)):
            request_func_kwargs = {}
        request_func_kwargs = Dict(request_func_kwargs)
        request_func_kwargs.setdefault("url", f"{self.base_url}/cgi-bin/media/uploadimg")
        request_func_kwargs.setdefault("method", f"POST")
        request_func_kwargs.setdefault("params", Dict())
        request_func_kwargs.params.setdefault("access_token", self.access_token)
        response = requests.request(**request_func_kwargs.to_dict())
        if Draft202012Validator({"type": "boolean", "const": True}).is_valid(
                isinstance(request_func_response_callable, Callable)):
            return request_func_response_callable(response, request_func_kwargs)
        if response.status_code == 200:
            if Draft202012Validator(
                    {
                        "type": "object",
                        "properties": {
                            "errcode": {"type": "integer", "const": 0},
                            "url": {"type": "string", "minLength": 1, "format": "uri"},
                            "required": ["errcode", "url"],
                        },
                    }
            ).is_valid(response.json()):
                return Dict(response.json()).url
        return None
