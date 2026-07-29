# -*- coding: utf-8 -*-

from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        # Aseguramos cargar el campo pos_config_ids en la carga de datos de pos.session
        if 'search_params' in result and 'fields' in result['search_params']:
            if 'pos_config_ids' not in result['search_params']['fields']:
                result['search_params']['fields'].append('pos_config_ids')
        return result

    def _get_pos_ui_product_product(self, params):
        """
        Filtra los productos a cargar en el POS frontend de modo que solo se envíen:
        1. Productos sin PDV específico seleccionado (disponibles para todos).
        2. Productos asignados explícitamente al PDV (pos.config) actual de esta sesión.
        """
        domain = params.get('search_params', {}).get('domain', [])
        pos_config_id = self.config_id.id
        
        custom_domain = [
            '|',
            ('pos_config_ids', '=', False),
            ('pos_config_ids', 'in', [pos_config_id])
        ]
        
        params['search_params']['domain'] = domain + custom_domain
        return super()._get_pos_ui_product_product(params)
