# -*- coding: utf-8 -*-
{
    'name': "Annexes rapport devis",

    'summary': """
        Annexes en fin du rapport devis""",

    'description': """
        Ajout d'un champ pour déposer des pièces jointes et les rajouter à la fin du rapport devis
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
    'depends': ['base','sale','mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order.xml',
        'views/mail_compose.xml',
        'report/report_sale_order.xml',
        'views/templates.xml',
    ],
}
