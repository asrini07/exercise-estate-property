from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'model estate property type'
    _order = "sequence desc"
    _inherit = "estate.mixin"

    sequence = fields.Integer(default=1)
    name = fields.Char(required=True, string="Name")
    property_ids = fields.One2many("estate.property", "property_type_id")
    property_count = fields.Integer(compute="_compute_property_count")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for vals in vals_list:
            self.env["estate.property.tag"].create(
                {
                    "name": vals.get("name"),
                }
            )
        return res
    
    def unlink(self):
        for record in self:
            # Cek apakah ada properti yang masih aktif dengan tipe ini
            linked_properties = self.env["estate.property"].search([("property_type_id", "=", record.id)])
            if any(prop.state not in ("new", "canceled") for prop in linked_properties):
                raise UserError(_("You cannot delete a property type linked to active properties!"))
        return super().unlink()
        # self.property_ids.state = "cancelled"
        # return super().unlink()

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