# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Annexedevis(models.Model):
    _name = 'annexe.devis'
    _description = 'Fichier en annexe devis'

    def get_current_devis(self):
        return self.id
    
    name = fields.Char()
    bp_file = fields.Image(string="Image")
    bp_devis_link = fields.Many2one('sale.order', string="Devis liée", default=get_current_devis)