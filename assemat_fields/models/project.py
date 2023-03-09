# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = 'project.project'

    bp_sale_count = fields.Integer(compute="_compute_count_sale")

    def _compute_count_sale(self):
        for record in self:
            record.bp_sale_count = self.env['sale.order'].search_count([('bp_worksite', '=', self.id)])
            
    #Fonctionnement V15 repris
    def action_show_timesheets_by_employee_invoice_type(self):
        view_id = self.env.ref('hr_timesheet.hr_timesheet_line_tree').id
        action = {
            'display_name': "Feuille de temps",
            'type': 'ir.actions.act_window',
            'res_model': 'account.analytic.line',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'is_timesheet': 1,
                'default_project_id': self.id,
                'search_default_groupby_employee': True,
            },
            'views': [[view_id, 'tree']],
            'view_type': 'tree',
            'view_mode': 'tree, form',
        }
        return action
    
    def action_view_analytic_account_entries(self):
        self.ensure_one()
        return {
            'res_model': 'account.analytic.line',
            'type': 'ir.actions.act_window',
            'name': "Marge brute",
            'domain': [('account_id', '=', self.analytic_account_id.id)],
            'views': [(self.env.ref('analytic.view_account_analytic_line_tree').id, 'list'),
                      (self.env.ref('analytic.view_account_analytic_line_form').id, 'form'),
                      (self.env.ref('analytic.view_account_analytic_line_graph').id, 'graph'),
                      (self.env.ref('analytic.view_account_analytic_line_pivot').id, 'pivot')],
            'view_mode': 'tree,form,graph,pivot',
            'context': {'search_default_group_date': 1, 'default_account_id': self.analytic_account_id.id}
        }