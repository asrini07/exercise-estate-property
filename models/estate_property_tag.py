from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'model estate property tag'
    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "Tag name should be unique")
    ]

    name = fields.Char(required=True, string="Name")