# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

import logging
_logger = logging.getLogger(__name__)

class CustomWorksiteSheet(models.Model):
    _name = 'custom.worksite.sheet'

    name = fields.Char(string="Titre rapport")
    bp_color = fields.Char(string="Couleur rapport")