# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError,UserError,Warning

import logging
_logger = logging.getLogger(__name__)


class OuvrageSetting(models.TransientModel):
    _inherit = 'res.config.settings'
    
    BP_COEFF_FAB = fields.Float(string="Coefficient fabrication")
    BP_COEFF_MATERIAL = fields.Float(string="Coefficient matériel")
    BP_HOURLY_RATE = fields.Float(string="Taux horaire")

    def set_values(self):
        res = super(OuvrageSetting, self).set_values()
        self.env['ir.config_parameter'].set_param('ouvrage.BP_COEFF_FAB', self.BP_COEFF_FAB)
        self.env['ir.config_parameter'].set_param('ouvrage.BP_COEFF_MATERIAL', self.BP_COEFF_MATERIAL)
        self.env['ir.config_parameter'].set_param('ouvrage.BP_HOURLY_RATE', self.BP_HOURLY_RATE)
        return res

    def get_values(self):
        res = super(OuvrageSetting, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        inf_BP_COEFF_FAB = ICPSudo.get_param('ouvrage.BP_COEFF_FAB')
        inf_BP_COEFF_MATERIAL = ICPSudo.get_param('ouvrage.BP_COEFF_MATERIAL')
        inf_BP_HOURLY_RATE = ICPSudo.get_param('ouvrage.BP_HOURLY_RATE')
        res.update(
            BP_COEFF_FAB = inf_BP_COEFF_FAB,
            BP_COEFF_MATERIAL = inf_BP_COEFF_MATERIAL,
            BP_HOURLY_RATE = inf_BP_HOURLY_RATE,
        )
        return res
    
