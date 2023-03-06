# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
    _inherit = 'project.project'

    bp_sale_count = fields.Integer(compute="_compute_count_sale")

    def _compute_count_sale(self):
        for record in self:
            record.bp_sale_count = self.env['sale.order'].search_count([('bp_worksite', '=', self.id)])
            
    #Fonctionnement V15 repris
    def action_show_timesheets_by_employee_invoice_type(self):
        action = self.env["ir.actions.actions"]._for_xml_id("hr_timesheet.timesheet_action_all")
        #Let's put the chart view first
        new_views = []
        for view in action['views']:
            new_views.insert(0, view) if view[1] == 'list' else new_views.append(view)
        action.update({
            'display_name': "Feuille de temps",
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
                'search_default_groupby_employee': True,
                'search_default_groupby_timesheet_invoice_type': True
            },
            'views': new_views
        })
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