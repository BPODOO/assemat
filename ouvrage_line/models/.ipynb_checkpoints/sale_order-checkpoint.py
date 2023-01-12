# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    bp_coefficient = fields.Float(string="Coefficient", copy=True)
    bp_hourly_rate = fields.Float(string="Taux horaire", copy=True)
    bp_transport_cost = fields.Float(string="Frais de transport", copy=True)