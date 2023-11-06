from odoo import api, fields, models
from odoo.odoo.exceptions import UserError, ValidationError
from datetime import timedelta

# Data model representing a vehicle offer
# Contains fields like price, status, partner, property
# Also defines methods for refusing & accepting offers
class VehiclePropertyOffer(models.Model):
    _name = "vehicle.property.offer"
    _description = "Vehicle Property Offer Model"
    #_order = "Offer, description"

    # Offer price
    price = fields.Float("Price")
    
    # Is offer accepted/refused?
    status = fields.Selection(
        string = 'Status',
        selection = [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy = False,
    )
    
    partner_id = fields.Many2one("res.partner", string="Partner", required = True)
    property_id = fields.Many2one("vehicle.property", string="Property", required = True)
    property_type_id = fields.Many2one("vehicle.property.type", related = "property_id.property_type_id", string = "Property Type", store=True)

    validity = fields.Integer("Validity (days)", default = 7)

    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # Define conditions for offer validity
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date or fields.Datetime.now()).date() + timedelta(days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - (record.create_date or fields.Datetime.now()).date()).days

    def accept_offer(self):
        for record in self:
            if record.status != False:
                raise UserError("This offer has already been handled.")
            else:
                for offer in self.property_id.offer_ids:
                    if offer.status == "accepted":
                        raise UserError("Another offer have been accepted!")
                # Update offer status & other parameters for accepted offer
                record.status = "accepted"
                record.property_id.state = "offer_accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
        return True

    def refuse_offer(self):
        for record in self:
            if record.status != False:
                raise UserError("This offer has already been handled.")
            else:
                record.status = "refused"
        return True

    @api.model
    def create(self, vals):
        # When new offer is created
        # Gather current vehicle record
        current_property = self.env['vehicle.property'].browse(vals['property_id'])
        
        # Raise an error if new price is less than record price
        if vals['price'] < current_property.best_price:
            raise ValidationError("Price can't be lower then the best offer!")
        
        current_property.state = "offer_received"
        
        # Create new vehicle property offer
        return super().create(vals)

    _sql_constraints = [
        ("check_price", "check(price > 0)", "The price must be positive"),
    ]