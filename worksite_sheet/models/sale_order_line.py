# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    bp_is_select = fields.Boolean(string="Is Select", default=False)
    bp_is_select_bis = fields.Boolean(related="bp_is_select", readonly=False)
    bp_reload = fields.Boolean()
        