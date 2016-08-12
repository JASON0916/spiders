import logging
from ebay.models.EbayProduct import EbayProduct
from ebay.models import DBSession
from sqlalchemy.exc import SQLAlchemyError
from scrapy.exceptions import DropItem


class Pipeline(object):
    session = None

    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        try:
            data = EbayProduct(**item)
        except KeyError:
            raise DropItem

        try:
            self.session.add(data)
            self.session.commit()
            logging.info('add data {}'.format(data))
        except (SQLAlchemyError, Exception) as exc:
            logging.error(exc.message)
            self.session.rollback()

    def close_spider(self, spider):
        self.session.close()
