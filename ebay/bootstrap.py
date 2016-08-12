# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import (Table, Column, Integer,
                        String, Float, DateTime,
                        MetaData, UniqueConstraint, Index)
from ebay.models import POSTGRE_ENGINE

meta = MetaData()

EbayProduct = Table('ebay_product', meta,
                    Column('id', Integer, autoincrement=True, primary_key=True),
                    Column('section', String(100), default=''),
                    Column('name', String(100), nullable=False, default=''),
                    Column('picture', String(200), default=''),
                    Column('create_date', String(20), nullable=False, default=''),
                    Column('price', Float, default=0.0),
                    Column('price_unit', String(10), default=''),
                    Column('seller', String(50), default=''),
                    Column('seller_href', String(200), default=''),
                    Column('shipping_price', Float, default=0.0),
                    Column('shipping_unit', String(10), default=''),
                    Column('href', String(200), default=''),
                    Column('created_at', DateTime,
                           default=datetime.datetime.now,
                           onupdate=datetime.datetime.now),
                    Index('eb_name', 'name'),
                    Index('eb_create_date', 'create_date'),
                    Index('eb_seller', 'seller', 'seller_href'),
                    UniqueConstraint('name', 'seller')
                    )

meta.drop_all(POSTGRE_ENGINE)
meta.create_all(POSTGRE_ENGINE)
