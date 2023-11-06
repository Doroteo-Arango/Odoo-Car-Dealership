from odoo import fields, models

# Data model for tags used to describe vehicle
class VehiclePropertyTag(models.Model):
    _name = "vehicle.property.tag"
    _description = "Vehicle Property Tag Model"
    _order = "name"

    name = fields.Char("Name", required = True)
    color = fields.Integer("Color")

    _sql_constraints = [
        ("check_name", "UNIQUE(name)", "The name must be unique!"),
    ]