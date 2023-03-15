from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class ReportWorksiteSheet(models.AbstractModel):
    _name = "report.worksite_sheet.report_worksite_sheet_document"
    _description = "Fiche de chantier"
    
    #Déclenchement lors de l'impression
    def _get_report_values(self, docids, data=None):
        
        materials_lines = self.env['material.line'].search([['bp_sale_order_line_id', 'in', data['data']['sale_line_ids']]])
        materials_lines_group = self.group_materials_by_sale_order_line(materials_lines)
        return {
            'doc_ids' : docids,
            # 'docs': docs,
            'sale_lines': self.env['sale.order.line'].browse(data['data']['sale_line_ids']),
            'materials_lines': materials_lines_group,
            'ouvrage_lines': self.env['ouvrage.line'].browse(data['data']['ouvrage_line_ids']),
            'project_id': self.env['project.project'].browse(data['data']['project_id']),
        }
    
    def group_materials_by_sale_order_line(self,records):
        materials_group = {}
        for record in records:
            key = record.bp_sale_order_line_id.name
            material_line = {'qty_total': 0, 'lines': []}
            if key in materials_group.keys():
                materials_group[key]['qty_total'] += record.bp_qty
                materials_group[key]['lines'].append(record)
            else:
                materials_group[key] = {'qty_total': record.bp_qty, 'lines': [record]}
        return materials_group
            