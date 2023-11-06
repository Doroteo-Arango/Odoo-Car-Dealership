from odoo import fields, models

# Allow users to link to vehicles that they are associated with as sellers
class User(models.Model):
    # Extend user model by inheriting res.users
    _inherit = "res.users"

    property_ids = fields.One2many("vehicle.property", 
                                   "seller_id", 
                                   string='Properties', 
                                   domain=[("state", "in", ["new", "offer_received"])]
                                   )