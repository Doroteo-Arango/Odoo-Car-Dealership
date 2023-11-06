from odoo import api, fields, models
from odoo.odoo.exceptions import UserError, ValidationError
from odoo.odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta

# Data model representing vehicle listings for sale
class VehicleProperty(models.Model):
    _name = "vehicle.property"
    _description = "Vehicle Property Model"
    _order = "id, description"

    # Define required fields to describe vehicle listing
    name = fields.Char("Name", required = True)
    description = fields.Text("Description")
    fuel_type = fields.Char("Fuel Type")
    date_availability = fields.Date("Available From", default = lambda self: fields.Datetime.now()+relativedelta(months=3), copy = False)
    expected_price = fields.Float("Expected Price", required = True)
    selling_price = fields.Float("Selling Price", readonly = True, copy = False)
    seats = fields.Integer("Seats", default = 2)
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string = 'Status',
        selection = [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        default = 'new',
        required=True,
        copy=False,
    )
    # REMINDER: Many2one is used to link another record from another model to the record currently being edited
    property_type_id = fields.Many2one("vehicle.property.type", string="Property Type")
    tag_ids = fields.Many2many("vehicle.property.tag", string="Tags")
    # REMINDER: One2many  is used to display the existing relations between a record on the current model and multiple records from another model
    offer_ids = fields.One2many("vehicle.property.offer", "property_id", string="Offers")
    seller_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)

    # Calculate best offer based upon current offers
    best_price = fields.Float("Best Offer", compute = "_compute_best_price")

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(self.offer_ids.mapped("price"), default = 0)

    def finish_sale(self):
        for record in self:
            if record.state != "offer_accepted":
                raise UserError("An offer must be accepted!")
            else:
                record.state = "sold"
        return True

    def cancel_sale(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold Properties can't be canceled!")
            else:
                record.state = "canceled"
        return True
    
    _sql_constraints = [
        ("check_expected_price", "check(expected_price > 0)", "The expected price must be positive"),
        ("check_selling_price", "check(selling_price >= 0)", "The selling price must be positive"),
    ]

    # Ensure selling price is positive
    @api.constrains("selling_price","expected_price")
    def _check_selling_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_rounding=0.01)
                and float_compare(record.selling_price, record.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ) :
                raise ValidationError ("The selling price must be at least 90% of the expected price!")

    # Ensure that a property with a valid offer cannot be deleted unless offer is reviewed
    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_proper(self):
        for record in self:
            if record.state in ("new", "canceled"):
                return True
            else:
                raise UserError("A property with a valid offer can not be deleted!")