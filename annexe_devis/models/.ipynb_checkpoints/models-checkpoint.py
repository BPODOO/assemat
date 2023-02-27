# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    bp_upload_annexes = fields.One2many('annexe.devis','bp_devis_link')
        


