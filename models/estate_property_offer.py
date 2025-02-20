from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'model estate property offer'
    _rec_name = "property_id"
    #ke generate ke table tapi kalau make api constrain tidak makanya disarankan make api constrain
    # _sql_constraints = [
    #     ('check_offer_price', 'CHECK(price > 0)', 'Expected price must be strictly positive!')
    # ]

    price = fields.Float()
    status = fields.Selection([
        ('new', 'New'),
        ('onprogress', 'On Progress'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", invers="_inverse_date_deadline")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        # for rec in self:
        #     rec.date_deadline = fields.Date.today() + relativedelta(days=rec.validity)
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        # for rec in self:
        #     rec.validity = (rec.date_deadline - fields.Date.today).days
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def action_accept(self):
        # self.ensure_one()
        # if "accepted" in self.property_id.offer_ids.mapped('status'):
        #     raise UserError(_("Already accepted by partner"))
        # self.status = "accepted"
        # self.property_id.state = 'accepted'
        # self.property_id.selling_price = self.price
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("Text error"))
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id.id

    def action_refuse(self):
        self.ensure_one()
        self.status = "refused"

    @api.constrains("price")
    def _check_constraints(self):
        for offer in self:
            if offer.price < 1000:
                raise ValidationError(_("Offering Price can not be lower than  1.000"))

    
