from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
from datetime import datetime
import time
import pytz

class ReportProfiDetails(models.AbstractModel):
    _name = "report.report_profi_details.report_profitability_details"
    _description = "Rapport rentabilité détaillé"
    
        #Déclenchement lors de l'impression
    def _get_report_values(self, docids, data=None):
        list_chantier = []
        project_ids = self.env['project.project'].search([['id','in',docids]])
        for project in project_ids:
            sale_order = self.env['sale.order'].search([['bp_worksite','=',project.id],['state','=','sale']])
            sections_sale_order = self.list_sections(sale_order.order_line)
            fabrication_lines = self.env['fabrication'].search([['bp_sale_order_line_id', 'in', sale_order.order_line.ids]])
            materials_lines = self.env['material.line'].search([['bp_sale_order_line_id', 'in', sale_order.order_line.ids]])
            materials_lines_sort = materials_lines.sorted(key=lambda x: x.bp_sale_order_line_id.sequence)
            materials_lines_group = self.group_materials_by_sale_order_line(materials_lines_sort,fabrication_lines)
            _logger.info(materials_lines_group)
            _logger.info(sections_sale_order)
            chantier = {
                'name_chantier': project.name,
                'client': project.partner_id.name,
                'objet_section': sections_sale_order,
                'supplies': materials_lines_group,
                'revenus': self.format_revenue(sale_order),
            }
            list_chantier.append(chantier)
            
        return {
            'list_chantier': list_chantier,
            'date_creation_report': self._get_datetime_fr(),
            'format_with_thousands_sep': self._format_with_thousands_sep,
        }
            
    def _get_datetime_fr(self):
        tz_IN = pytz.timezone('Europe/Paris')
        now_FR = datetime.now(tz_IN) # Heure au fuseau horaire de Paris
        return now_FR.strftime('%d/%m/%Y %H:%M')   
    
    def group_materials_by_sale_order_line(self,records,fabrications):
        materials_group = {}
        for record in records:
            key = record.bp_sale_order_line_id.name +'_'+ str(record.bp_sale_order_line_id.id)
            if key in materials_group.keys():
                _logger.info(materials_group[key])
                materials_group[key]['lines'].append(record)
            else:
                materials_group[key] = {'lines': [record]}
            _logger.info(materials_group)
            materials_group[key]['qty_mo_previ'] = record.bp_sale_order_line_id.product_uom_qty
            materials_group[key]['cost_mo_previ'] = record.bp_sale_order_line_id.bp_total_cost_mo
            materials_group[key]['qty_mo_actual'] = record.bp_sale_order_line_id.bp_task_id.effective_hours
            materials_group[key]['cost_mo_actual'] = abs(sum(record.bp_sale_order_line_id.bp_task_id.timesheet_ids.mapped('amount')))
        return materials_group      
            
    def list_sections(self, sale_order_line):
        cpt = 1
        objet_sections = {}
        for section in sale_order_line:
            material_lines_exist = self.env['material.line'].search([['bp_sale_order_line_id','=',section.id]])
            if section.display_type == "line_section":
                objet_sections[cpt] = section.name
            elif(material_lines_exist):
                cpt += 1
        return objet_sections
    
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