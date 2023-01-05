# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    bp_worksite = fields.Many2one('project.project', string="Chantier", copy=False)
    
    @api.onchange('bp_worksite')
    def _onchange_worksite(self):
        self.partner_id = self.bp_worksite.partner_id
        self.analytic_account_id = self.bp_worksite.analytic_account_id