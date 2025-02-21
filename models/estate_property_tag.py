from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'model estate property tag'
    _inherit = "estate.mixin"
    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "Tag name should be unique")
    ]
    _order = "name desc"
 

    name = fields.Char(required=True, string="Name")
    color = fields.Integer()
