# -*- coding: utf-8 -*-
{
    'name': 'Restricción de Productos por PDV',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Delimita la disponibilidad de productos a puntos de venta específicos según la compañía.',
    'author': 'TQ',
    'depends': [
        'point_of_sale',
        'product',
    ],
    'data': [
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
