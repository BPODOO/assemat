# -*- coding: utf-8 -*-
{
    'name': "Report de la description SO dans les BL",

    'summary': """
        Affichage de la description des lignes des SO dans les lignes "Opérations" des BL
    """,

    'description': """
        Personnalisation de la vue formulaire des BL pour :
        - Ajouter la description du SO
    """,

    'author': "BeProject",
    'website': "https://beproject.fr/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock','sale_stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views_stock_picking.xml',
    ],
}