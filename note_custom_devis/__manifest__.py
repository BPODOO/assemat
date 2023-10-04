# -*- coding: utf-8 -*-
{
    'name': "Note personnalisée Devis",

    'summary': """
        Ajouter des images/textes dans les notes des devis""",

    'description': """
        Ajouter des images/textes dans les notes sur les devis et les rapports de devis
    """,

    'author': "BeProject",
    'website': "https://beproject.fr/",
    "license": "LGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views_sale_order_line.xml',
        'report/report_saleorder_document.xml',
        'views/templates.xml',
    ],
    'assets': {
       'web.assets_backend': [
           'note_custom_devis/static/src/components/**/*',
       ],
    },
}
