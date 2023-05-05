# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    ## Lien avec la ligne de vente pour savoir d'où provient cette tâche
    bp_sale_line_origin_task = fields.Many2one('sale.order.line', string="Ligne de vente d'origine", readonly=True, copy=False, help="Ligne de vente à l'origine de la création de la tâche", ondelete='cascade')
    
    #OVERRIDE de la fonction unlink pour refresh la création de tâche en cas de suppression
    def unlink(self):
        order_ids = set(order.bp_sale_line_origin_task.order_id.id for order in self)
        unique_order_ids = list(order_ids)
        res = super(ProjectTask, self).unlink()
        self.env['sale.order'].browse(unique_order_ids)._compute_task_to_create()
        return res