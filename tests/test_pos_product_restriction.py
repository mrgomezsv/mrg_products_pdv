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
        """ Verificar el dominio de productos que se cargan en el POS (Odoo 20) """
        domain = self.env['product.template']._load_pos_data_domain({'pos.config': self.pos_config_a1})
        loaded_templates = self.env['product.template'].with_company(self.company_a).search(domain)

        # Validar inclusión/exclusión de productos en PDV A1
        self.assertIn(self.product_restricted_a1, loaded_templates, "El producto A1 debe cargarse en el PDV A1")
        self.assertIn(self.product_global_a, loaded_templates, "El producto Global debe cargarse en cualquier PDV de su compañía")
        self.assertNotIn(self.product_restricted_a2, loaded_templates, "El producto A2 NO debe cargarse en el PDV A1")
