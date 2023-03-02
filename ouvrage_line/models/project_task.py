# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    ## Lien avec la ligne de vente pour savoir d'où provient cette tâche
    bp_sale_line_origin_task = fields.Many2one('sale.order.line', string="Ligne de vente à l'origine", readonly=True, copy=False, help="Ligne de vente à l'origine de la création de la tâche", ondelete='cascade')