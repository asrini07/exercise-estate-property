from odoo import models, fields, api, _

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'model estate property type'
    _order = "sequence desc"

    sequence = fields.Integer(default=1)
    name = fields.Char(required=True, string="Name")
    property_ids = fields.One2many("estate.property", "property_type_id")
    property_count = fields.Integer(compute="_compute_property_count")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    @api.depends("property_ids")
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)

    def action_open_property_ids(self):
        return {
            "name": _("Related Properties"),
            "type": "ir.actions.act_window",
            "view_mode": "tree,form",
            "res_model": "estate.property",
            "target": "current",
            "domain": [("property_type_id", "=", self.id)],
            "context": {"default_property_type_id": self.id}
        }