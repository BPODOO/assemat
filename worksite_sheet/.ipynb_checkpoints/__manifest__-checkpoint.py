# -*- coding: utf-8 -*-
{
    'name': "Fiche de chantier",

    'summary': """
        Imprime une fiche de chantier
        """,

    'description': """
        Imprime une fiche de chantier en fonction des conditions que l'on souhaite.
        """,

    'author': "BeProject",
    'website': "https://beproject.fr/",
    'license': "GPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        
        'wizard/views_worksite_sheet.xml',
        'report/report_worksite_sheet.xml',
        'report/report_worksite_call.xml',
    ],
}
