# -*- coding: utf-8 -*-
{
    'name': "Liste description",

    'summary': """
        Liste description""",

    'description': """
        Liste de choix pour les descriptions des feuilles de temps
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
    'depends': ['base','account','timesheet_grid'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
