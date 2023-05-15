from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
from datetime import datetime
import time
import pytz

class ReportProfi(models.AbstractModel):
    _name = "report.report_profi.report_profitability"
    _description = "Rapport rentabilité"
    
    #Déclenchement lors de l'impression
    def _get_report_values(self, docids, data=None):
        list_chantier = []
        project_ids = self.env['project.project'].search([['id','in',docids]])
        for project in project_ids:
            sale_order = self.env['sale.order'].search([['bp_worksite','=',project.id],['state','=','sale']])
            account_analytic_lines_without_account = self.env['account.analytic.line'].search([['account_id','=',project.analytic_account_id.id],['general_account_id', '=', False]])
            fabrication_lines_sale_order = self.env['fabrication'].search([['bp_sale_order_id','in',sale_order.ids],['bp_cost','!=',0.0]])
            # On récupère tout les types de travaux dans le champ selection bp_timesheet_description_id
            list_desc_dict = dict(self.env['account.analytic.line'].fields_get(allfields=['bp_list_desc']))['bp_list_desc']['selection']
            list_desc_dict_new = self.env['timesheet.description'].search([])
            list_desc = [x[1].upper() for x in list_desc_dict]
            list_desc_new = [x.upper() for x in list_desc_dict_new.mapped('name')]
            # Récupération des types de travaux ayant un coût différent de 0
            type_works_fabrication = self.all_upper(fabrication_lines_sale_order.mapped('name'))
            type_works_ccount_analytic_lines = self.all_upper(account_analytic_lines_without_account.mapped('name'))
            # Type de travaux ayant des données
            type_works = list(set(type_works_fabrication + type_works_ccount_analytic_lines))
            type_works_sorted_by_bp_timesheet_description_id = list_desc + type_works
            type_works_sorted_by_bp_timesheet_description_id_without_duplicates = list(dict.fromkeys(type_works_sorted_by_bp_timesheet_description_id))
            # Lignes de fabrication du devis regroupé par type de travaux
            fabrication_lines_sale_order_group_by_type_works = fabrication_lines_sale_order._read_group(domain=[('bp_cost','!=',0.0),('bp_sale_order_id','in',sale_order.ids),('bp_sale_order_id.state','=','sale')], fields=['bp_sale_order_id','name','bp_duration','bp_cost'], groupby=['name'])
            # Lignes analytiques du devis regroupé par type de travaux
            account_analytic_lines_without_account_group_by_type_works = account_analytic_lines_without_account._read_group(domain=[('account_id','=',project.analytic_account_id.id),('general_account_id', '=', False)], fields=['name','unit_amount','amount'], groupby=['name'])

            # Récupération des dépenses des comptes VOYAGES ET DEPLACEMENT & CARBURANT
            expenses_travels_account = self.env['account.analytic.line'].search([['account_id','=',project.analytic_account_id.id],['general_account_id.code', '=', '62510000']])
            expenses_fuel_account = self.env['account.analytic.line'].search([['account_id','=',project.analytic_account_id.id],['general_account_id.code', '=', '60614000']])

            # Récupération du suivi du matériel du chantier
            material_line_group_by_sale_order_lines = self.env['material.line']._read_group(domain=[('bp_sale_order_id','in',sale_order.ids),('bp_sale_order_id.state','=','sale')], fields=['bp_sale_order_line_id','bp_qty','bp_cost','bp_cost_actual','bp_qty_used'], groupby=['bp_sale_order_line_id'])
            
            chantier = {
                'name_chantier': project.name,
                'client': project.partner_id.name,
                'type_travaux': type_works_sorted_by_bp_timesheet_description_id_without_duplicates,
                'mo_previ': self.format_group_by_fabrication(fabrication_lines_sale_order_group_by_type_works),
                'mo_actual': self.format_group_by_analytic(account_analytic_lines_without_account_group_by_type_works),
                'expenses_travels': self.format_expenses(expenses_travels_account),
                'expenses_fuel': self.format_expenses(expenses_fuel_account),
                'supplies': self.format_group_by_supplies(material_line_group_by_sale_order_lines),
                'revenus': self.format_revenue(sale_order),
            }
            list_chantier.append(chantier)
            _logger.info(chantier)

        return {
            'list_chantier': list_chantier,
            'date_creation_report': self._get_datetime_fr(),
            'format_with_thousands_sep': self._format_with_thousands_sep
        }
        
        
    def _get_datetime_fr(self):
        tz_IN = pytz.timezone('Europe/Paris')
        now_FR = datetime.now(tz_IN) # Heure au fuseau horaire de Paris
        return now_FR.strftime('%d/%m/%Y %H:%M')
    
    def all_upper(self,my_list):
        return [x.upper() for x in my_list]
    
    def format_group_by_fabrication(self,my_list):
        list_new_format = {}
        if my_list:
            for el in my_list:
                name_works = el['name'].upper()
                list_new_format[name_works] = {'duration': el['bp_duration'], 'cost': el['bp_cost']}
            
        return list_new_format
    
    def format_group_by_analytic(self,my_list):
        list_new_format = {}
        if my_list:
            for el in my_list:
                name_works = el['name'].upper()
                list_new_format[name_works] = {'duration': el['unit_amount'], 'cost': abs(el['amount'])}
            
        return list_new_format
    
    def format_group_by_supplies(self,my_list):
        list_new_format = {}
        if my_list:
            for el in my_list:
                sale_order_line = self.env['sale.order.line'].browse(el['bp_sale_order_line_id'][0])
                sale_order = sale_order_line.order_id
                name_works = sale_order_line.name[0].upper() + sale_order_line.name[1:]
                list_new_format[name_works] = {'cost_previ': el['bp_cost'],'cost_actual': el['bp_cost_actual']}
            
        return list_new_format
    
    def format_expenses(self,my_expenses):
        list_new_format = {}
        sum_expense_cost = 0.0
        sum_expense_qty = 0.0
        if my_expenses:
            for expense in my_expenses:
                name_account = expense.general_account_id.name
                sum_expense_cost += expense.amount
                sum_expense_qty += expense.unit_amount

            list_new_format[name_account] = {'duration': sum_expense_qty, 'cost': abs(sum_expense_cost)}
            
        return list_new_format
                                                    
    
    def format_revenue(self, my_revenus):
        list_new_format = {}
        if my_revenus:
            for revenu in my_revenus:
                invoice_sale_order = self.env['account.move'].search([['invoice_origin','=',revenu.name],['state','=','posted']])
                total_invoice_sale_order = invoice_sale_order.mapped('amount_untaxed') if invoice_sale_order else [0.0]
                name_revenu = revenu['name'].upper()
                list_new_format[name_revenu] = {'cost_previ': revenu['amount_untaxed'], 'cost_actual': sum(total_invoice_sale_order)}
        return list_new_format
    
    def _format_with_thousands_sep(self, number):
        return "{:,.2f}".format(number).replace(',', ' ')
                                                    
        