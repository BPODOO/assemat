# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = 'project.project'

    bp_sale_count = fields.Integer(compute="_compute_count_sale")

    bp_sale_order_ids = fields.One2many('sale.order', 'bp_worksite', string="Bon de commande(s)", readonly=True)
    
    ############### ETAT DES LIEUX ##################
    #-- Materiel --#
    bp_material_cost_previ = fields.Float(string="Coût prévisionnel", compute="_compute_material_cost_previ_actual")
    bp_material_cost_actual = fields.Float(string="Coût actuel", compute="_compute_material_cost_previ_actual")
    bp_material_percentage = fields.Float(string="%")
    #-- Main d'oeuvre --#
    bp_mo_cost_previ = fields.Float(string="Coût prévisionnel", compute="_compute_mo_cost_previ_actual")
    bp_mo_cost_actual = fields.Float(string="Coût actuel", compute="_compute_mo_cost_previ_actual")
    bp_mo_percentage = fields.Float(string="%")
    #-- Coût total --#
    bp_total_cost_previ = fields.Float(string="Coût prévisionnel", compute="_compute_total_cost_previ_actual")
    bp_total_cost_actual = fields.Float(string="Coût actuel", compute="_compute_total_cost_previ_actual")
    bp_total_percentage = fields.Float(string="%")
    #-- Marge --#
    bp_margin_previ = fields.Float(string="Marge prévisionnel", compute="_compute_margin_previ_actual")
    bp_margin_actual = fields.Float(string="Marge actuel", compute="_compute_margin_previ_actual")
    
    def _compute_material_cost_previ_actual(self):
        order_ids = self.env['sale.order'].search([('bp_worksite','=',self.id),('state','=','sale')]).ids
        material_lines = self.env['material.line'].search([['bp_sale_order_id.id','in',order_ids]])
        list_bp_cost = list(map(lambda line: line.bp_cost,material_lines))
        list_bp_cost_actual = list(map(lambda line: line.bp_cost_actual,material_lines))
        self.bp_material_cost_previ = sum(list_bp_cost)
        self.bp_material_cost_actual = sum(list_bp_cost_actual)
        self.bp_material_percentage = (self.bp_material_cost_actual*100) / self.bp_material_cost_previ
        
    def _compute_mo_cost_previ_actual(self):
        order_ids = self.env['sale.order'].search([('bp_worksite','=',self.id),('state','=','sale')]).ids
        sale_order_lines = self.env['sale.order.line'].search([['order_id','in',order_ids]])
        account_analytic_lines = self.env['account.analytic.line'].search([['account_id','=',self.analytic_account_id.id]])
        list_total_cost_mo = list(map(lambda line: line.bp_total_cost_mo,sale_order_lines))
        list_unit_amount = list(map(lambda line: line.unit_amount,account_analytic_lines))
        self.bp_mo_cost_previ = sum(list_total_cost_mo)
        self.bp_mo_cost_actual = self.allocated_hours - sum(list_unit_amount)
        self.bp_mo_percentage = (self.bp_mo_cost_actual*100) / self.bp_mo_cost_previ
        
    @api.depends('bp_mo_cost_actual','bp_material_cost_actual','bp_material_cost_previ','bp_mo_cost_previ')
    def _compute_total_cost_previ_actual(self):
        self.bp_total_cost_previ = self.bp_material_cost_previ + self.bp_mo_cost_previ
        self.bp_total_cost_actual = self.bp_material_cost_actual + self.bp_mo_cost_actual
        self.bp_total_percentage = (self.bp_total_cost_actual*100) / self.bp_total_cost_previ
    
    @api.depends('bp_total_cost_previ','bp_total_cost_actual')
    def _compute_margin_previ_actual(self):
        order_ids = self.env['sale.order'].search([('bp_worksite','=',self.id),('state','=','sale')])
        list_amount_untaxed = list(map(lambda order: order.amount_untaxed,order_ids))
        self.bp_margin_previ = sum(list_amount_untaxed) - self.bp_total_cost_previ
        self.bp_margin_actual = sum(list_amount_untaxed) - self.bp_total_cost_actual
        
                                        
    
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