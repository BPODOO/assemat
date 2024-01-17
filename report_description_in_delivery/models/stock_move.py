# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'
    
    bp_description = fields.Text(
        related='sale_line_id.name',
        string="Description",
        store=True, 
        readonly=True
    )