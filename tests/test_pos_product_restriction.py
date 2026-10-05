# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestMrgProductsPdv(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 1. Crear Compañías de prueba
        cls.company_a = cls.env['res.company'].create({'name': 'Compañía Test A'})
        cls.company_b = cls.env['res.company'].create({'name': 'Compañía Test B'})

        # 2. Crear Puntos de Venta (pos.config) para Compañía A
        cls.pos_config_a1 = cls.env['pos.config'].create({
            'name': 'PDV A1',
            'company_id': cls.company_a.id,
        })
        cls.pos_config_a2 = cls.env['pos.config'].create({
            'name': 'PDV A2',
            'company_id': cls.company_a.id,
        })

        # 3. Crear Punto de Venta para Compañía B
        cls.pos_config_b1 = cls.env['pos.config'].create({
            'name': 'PDV B1',
            'company_id': cls.company_b.id,
        })

        # 4. Crear Productos de prueba en Compañía A
        cls.product_restricted_a1 = cls.env['product.template'].create({
            'name': 'Producto Restringido a PDV A1',
            'available_in_pos': True,
            'company_id': cls.company_a.id,
            'pos_config_ids': [(6, 0, [cls.pos_config_a1.id])],
        })

        cls.product_restricted_a2 = cls.env['product.template'].create({
            'name': 'Producto Restringido a PDV A2',
            'available_in_pos': True,
            'company_id': cls.company_a.id,
            'pos_config_ids': [(6, 0, [cls.pos_config_a2.id])],
        })

        cls.product_global_a = cls.env['product.template'].create({
            'name': 'Producto Global Compañía A',
            'available_in_pos': True,
            'company_id': cls.company_a.id,
            'pos_config_ids': False,
        })

    def test_01_domain_filtering_by_company(self):
        """ Verificar que el campo pos_config_ids filtre correctamente por compañía """
        # Obtener los PDVs disponibles para la plantilla del Producto A1
        available_pdvs = self.env['pos.config'].search([
            ('company_id', '=', self.product_restricted_a1.company_id.id)
        ])
        self.assertIn(self.pos_config_a1, available_pdvs)
        self.assertIn(self.pos_config_a2, available_pdvs)
        self.assertNotIn(self.pos_config_b1, available_pdvs)

    def test_02_pos_session_product_filtering(self):
        """ Verificar la lógica de filtrado de productos en la sesión del POS """
        # Crear una sesión para PDV A1
        session_a1 = self.env['pos.session'].create({
            'config_id': self.pos_config_a1.id,
            'user_id': self.env.user.id,
        })

        # Ejecutar el método herederado para obtener el dominio de productos
        params = {'search_params': {'domain': [('available_in_pos', '=', True)]}}
        session_a1._get_pos_ui_product_product(params)

        res_domain = params['search_params']['domain']

        # Buscar variantes resultantes aplicando el dominio generado por el módulo
        loaded_products = self.env['product.product'].search(res_domain)

        # Variantes de nuestros productos creados
        variant_a1 = self.product_restricted_a1.product_variant_id
        variant_a2 = self.product_restricted_a2.product_variant_id
        variant_global = self.product_global_a.product_variant_id

        # Validar inclusión/exclusión de productos en PDV A1
        self.assertIn(variant_a1, loaded_products, "El producto A1 debe cargarse en la sesión del PDV A1")
        self.assertIn(variant_global, loaded_products, "El producto Global debe cargarse en cualquier PDV de su compañía")
        self.assertNotIn(variant_a2, loaded_products, "El producto A2 NO debe cargarse en la sesión del PDV A1")
