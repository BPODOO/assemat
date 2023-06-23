# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TimesheetDescription(models.Model):
    _name = 'timesheet.description'
    
    _order = 'sequence'
    
    name = fields.Char(string="Nom", required=True)
    sequence = fields.Integer(default=10)
    
    bp_is_default = fields.Boolean(string="Par défaut", help="Cette ligne sera présente par défaut dans un ouvrage en prenant la durée par défaut")
    bp_default_time = fields.Float(string="Durée", help="Temps par défaut pour cette ligne")

    bp_product_ids = fields.Many2many('product.product', string="Réalisation")