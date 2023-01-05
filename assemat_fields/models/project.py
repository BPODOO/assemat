# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'

    bp_sale_count = fields.Integer(compute="_compute_count_sale")

    def _compute_count_sale(self):
        for record in self:
            record.bp_sale_count = self.env['sale.order'].search_count([('bp_worksite', '=', self.id)])