from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'model estate property'
    _order = "id desc"
    
    _sql_constraints = [
       ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive!') 
    ]

    def _default_date(self):
        return fields.Date.today()

    name = fields.Char(required=True, string="Name")
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=_default_date)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], )
    active = fields.Boolean(default=True, invisible="true")
    state = fields.Selection(
        [
            ("new", "New"),
            ("received", "Offer Received"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id=fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Sales Person")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    total_area = fields.Integer('Total Area', compute="_compute_total_area")
    best_price = fields.Float('Best Price', compute='_compute_best_price')

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offer_ids.mapped('price') or [0])

    @api.onchange('garden')
    def _onchange_garden(self):
        # if not self.garden:
        #     self.garden_area = 0
        #     self.garden_orientation = false
        for rec in self:
            if not rec.garden:
                rec.garden_area =0

    @api.onchange('date_availability')
    def _onchange_date_availability(self):
        for estate in self:
            if estate.date_availability and estate.date_availability < fields.Date.today():
                # return {
                #     "warning": {
                #         "title": _("Warning"),
                #         "message": _("My message")
                #     }
                # }
                raise ValidationError(_("Date availability set in the past"))

    # @api.constrains("selling_price")
    # def _check_constraints(self):
    #     for estate in self:
    #         if estate.selling_price < 1000000:
    #             raise ValidationError(_("Selling price can not be lower than  1.000.000"))

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for rec in self:
            if rec.selling_price > 0 and rec.selling_price < (rec.expected_price * 0.9):
                raise ValidationError(_("Selling price cannot be lower than 90% of the expected price!"))

    def action_sold(self):
        if "sold" in self.state:
            raise UserError(_("Already accepted by partner"))
        self.state = "sold"

    def action_cancel(self):
        self.state = "canceled"
    
