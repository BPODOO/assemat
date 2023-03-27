# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = 'project.project'
    
    def action_open_print_worksite_sheet(self):
        view_id = self.env.ref('worksite_sheet.view_print_worksite_sheet_bp').id
        
        sale_ids = self.bp_sale_order_ids.ids 

        # TO ACTIVE FINAL STEP -> Lorsqu'il n'y a pas de sale.order en Bon de commande on retourne une erreur
        #sale_ids = self.bp_sale_order_ids.filtered(lambda x: x.state == 'sale').ids
        # if not sale_ids: raise UserError("Aucune Bon de commande, fiche chantier impossible !")
        
        return {
            'name': 'Fiche de chantier',
            'type': 'ir.actions.act_window',
            'res_model': 'print.worksite.sheet',
            'context': {
                'default_bp_order_domain_ids': sale_ids,
                'default_bp_order_id': sale_ids[0],
                'default_bp_project_id': self.id,
            },
            'target': 'new',
            'view_id': view_id,
            'view_mode': 'form',
        }