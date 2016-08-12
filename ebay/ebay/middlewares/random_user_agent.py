#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.utils.project import get_project_settings
import random


class RandomUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        settings = get_project_settings()
        self.user_agent = settings.get('USER_AGENT_LIST', {})

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent)
        if ua:
            request.headers.setdefault('User-Agent', ua)