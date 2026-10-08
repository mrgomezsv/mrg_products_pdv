from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pos_config_ids = fields.Many2many(
        comodel_name='pos.config',
        string='Disponible en PDV',
        help='Seleccione los Puntos de Venta específicos donde estará disponible este producto. '
             'Si se deja vacío, el producto estará disponible en todos los PDV de la compañía.',
        domain="[('company_id', '=', company_id)]"
    )

    @api.model
    def _load_pos_data_domain(self, data):
        domain = super()._load_pos_data_domain(data)
        config = data.get('pos.config')
        if config:
            config_id = config.id if hasattr(config, 'id') else config
            domain += [
                '|',
                ('pos_config_ids', '=', False),
                ('pos_config_ids', 'in', [config_id])
            ]
        return domain
