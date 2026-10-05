# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_config_ids = fields.Many2many(
        comodel_name='pos.config',
        string='Disponible en PDV',
        help='Seleccione los Puntos de Venta específicos donde estará disponible este producto. '
             'Si se deja vacío, el producto estará disponible en todos los PDV de la compañía.',
        domain="[('company_id', '=', company_id)] if company_id else []"
    )
