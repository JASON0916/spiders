#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ebay.settings import POSTGRE_URL

POSTGRE_ENGINE = create_engine(POSTGRE_URL, echo=True)
DBSession = sessionmaker(bind=POSTGRE_ENGINE)
