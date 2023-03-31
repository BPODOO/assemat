from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)
import datetime
import time
import pytz

class ReportWorksiteSheet(models.AbstractModel):
    _name = "report.worksite_sheet.report_worksite_sheet_document"
    _description = "Fiche de chantier"
    
    #Déclenchement lors de l'impression
    def _get_report_values(self, docids, data=None):
        
        _logger.info(data['data']['objet_section'])
        fabrication_lines = self.env['fabrication'].search([['bp_sale_order_line_id', 'in', data['data']['sale_line_ids']]])
        materials_lines = self.env['material.line'].search([['bp_sale_order_line_id', 'in', data['data']['sale_line_ids']]])
        materials_lines_group = self.group_materials_by_sale_order_line(materials_lines,fabrication_lines)
        return {
            'doc_ids' : docids,
            # 'docs': docs,
            'date_now': datetime.datetime.now().astimezone(pytz.timezone('Europe/Berlin')).strftime("%d-%m-%Y %H:%M:%S"),
            'objet_section': data['data']['objet_section'],
            'sale_lines': self.env['sale.order.line'].browse(data['data']['sale_line_ids']),
            'materials_lines': materials_lines_group,
            'ouvrage_lines': self.env['ouvrage.line'].browse(data['data']['ouvrage_line_ids']),
            'project_id': self.env['project.project'].browse(data['data']['project_id']),
        }
    
    def group_materials_by_sale_order_line(self,records,fabrications):
        materials_group = {}
        # fabrication_totals = self._time_total_by_sale_order_line(fabrications)
        for record in records:
            key = record.bp_sale_order_line_id.name +'_'+ str(record.bp_sale_order_line_id.id)
            material_line = {'qty_total': 0, 'lines': [], 'time_total': 0}
            if key in materials_group.keys():
                materials_group[key]['qty_total'] += record.bp_qty
                materials_group[key]['lines'].append(record)
            else:
                materials_group[key] = {'qty_total': record.bp_qty, 'lines': [record]}
        # for fab_key in fabrication_totals:
        #     materials_group[fab_key]['time_total'] = fabrication_totals[fab_key]['time_total']
        return materials_group
            
    # def _time_total_by_sale_order_line(self,records):
    #     fabrication_group = {}
    #     for record in records:
    #         key = record.bp_sale_order_line_id.name
    #         fabrication_line = {'time_total': 0}
    #         if key in fabrication_group.keys():
    #             fabrication_group[key]['time_total'] += record.bp_duration
    #         else:
    #             fabrication_group[key] = {'time_total': record.bp_duration}
    #     return fabrication_group
        