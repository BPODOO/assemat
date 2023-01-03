# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    bp_list_desc = fields.Selection([('bureau dessin', 'bureau dessin'),('approvisionnement matériel', 'approvisionnement matériel'),('débit scie', 'débit scie'),('echantage', 'echantage'),("centre d'usinage", "centre d'usinage"),("montage en atelier", "montage en atelier"),("placage stratifié en presse", "placage stratifié en presse"),("placage stratifié pistolable", "placage stratifié pistolable"),("ponçage et finitions", "ponçage et finitions"),("vernissage et peinture", "vernissage et peinture"),("vernissage et peinture", "vernissage et peinture"),("emballage", "emballage"),("fabrication palette de transport", "fabrication palette de transport"),("chargement", "chargement"),("nettoyage atelier", "nettoyage atelier"),("évacuation des copeaux", "évacuation des copeaux"),("entretien atelier", "entretien atelier")])

    @api.onchange('bp_list_desc')
    def complete_description(self):
        for record in self:
            record['name'] = record.bp_list_desc