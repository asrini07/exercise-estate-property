from odoo import models, fields, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'model estate property type'
    _order = "sequence desc"

    sequence = fields.Integer(default=1)
    name = fields.Char(required=True, string="Name")
    property_ids = fields.One2many("estate.property", "property_type_id")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)