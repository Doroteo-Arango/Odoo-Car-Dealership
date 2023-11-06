from odoo import api, fields, models

# Data model for vehicle type
class VehiclePropertyType(models.Model):
    _name = "vehicle.property.type"
    _description = "Vehicle Property Type Model"
    _order = "sequence, name"

    name = fields.Char("Name", required = True)
    sequence = fields.Integer("Sequence", default = 1, help = "Used to order stages. Lower is better.")
    property_ids = fields.One2many("vehicle.property", "property_type_id", string="Vehicle")
    offer_ids = fields.One2many("vehicle.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer("Number of Offers", compute='_compute_offers') 

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique!"),
    ]

    @api.depends("offer_ids")
    # Count offers for current vehicle type
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # View offers for this vehicle type
    def action_view_offers(self):
        res = self.env.ref("estate.property_offer_action").read()[0]
        res["domain"] = [("id", "in", self.offer_ids.ids)]
        return res