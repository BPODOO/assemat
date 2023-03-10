# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    bp_is_select = fields.Boolean(string="Is Select", default=False, store=True)
