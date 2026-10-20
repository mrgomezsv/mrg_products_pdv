# -*- coding: utf-8 -*-
# Archivo obsoleto: ya no se importa (ver models/__init__.py).
#
# En Odoo 17 se filtraban los productos del POS con
# _loader_params_product_product / _get_pos_ui_product_product. Esos métodos
# no existen en Odoo 20 y el filtro ahora vive en
# product.template._load_pos_data_domain (models/product_template.py).
# Se puede borrar este archivo.
