# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    
    def action_open_ouvrage_line(self):
        _logger.info("OPEN OUVRAGE LINE")
        _logger.info(self.env.context)
        _logger.info(self)
        _logger.info(self.order_id)