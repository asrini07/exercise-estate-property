from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'model estate property tag'

    name = fields.Char(required=True, string="Name")