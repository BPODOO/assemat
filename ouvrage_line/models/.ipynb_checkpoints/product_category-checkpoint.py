# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    bp_is_furniture = fields.Boolean(string="Est une fourniture", copy=False, 
                                     help="Permet de savoir si la catégorie d'article est de type fourniture, utile pour le tri du matériel d'ouvrage")