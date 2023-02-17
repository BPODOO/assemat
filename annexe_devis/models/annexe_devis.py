# -*- coding: utf-8 -*-

from odoo import models, fields, api


class annexe_devis(models.Model):
    _name = 'annexe.devis'
    _description = 'Fichier en annexe devis'

    name = fields.Char()
    bp_file = fields.Binary(string="Fichier")