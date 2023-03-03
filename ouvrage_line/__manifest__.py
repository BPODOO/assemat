# -*- coding: utf-8 -*-
{
    'name': "Ouvrage",

    'summary': """
        Permet le calcul d'une ligne de vente""",

    'description': """
        Propose une interface de calcul pour le prix d'une prestation (ligne de vente) en fonction de plusieurs paramètres.
    """,

    'author': "BeProject",
    'website': "https://beproject.fr/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    
    # any module necessary for this one to work correctly
    'depends': ['base','sale','list_timesheet','assemat_fields'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views_sale_order.xml',
        'views/views_ouvrage_line.xml',
        'views/views_material_line.xml',
        'views/views_material_line_associated.xml',
        'views/views_fabrication.xml',
        'views/views_project.xml',
        
        'views/views_config_ouvrage.xml',
        
        'views/views_product_category.xml',
        
        'views/templates.xml',
    ],
}
