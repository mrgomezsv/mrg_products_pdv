# -*- coding: utf-8 -*-
from odoo import models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _get_availlable_product_domain(self):
        domain = super()._get_availlable_product_domain()
        custom_domain = [
            '|',
            ('product_tmpl_id.pos_config_ids', '=', False),
            ('product_tmpl_id.pos_config_ids', 'in', [self.id])
        ]
        return domain + custom_domain
