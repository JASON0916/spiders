#!/usr/bin/env python                                                                                                                                                
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# POSTGRE_URL = 'postgresql+psycopg2://openerp:openerp@localhost:5432/openerp'
POSTGRE_URL = 'mysql://root:@localhost:3306/openerp'

POSTGRE_ENGINE = create_engine(POSTGRE_URL, echo=True)
DBSession = sessionmaker(bind=POSTGRE_ENGINE)
