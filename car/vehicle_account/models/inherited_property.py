#from odoo import Command

from odoo import models

class InheritedProperty(models.Model):
	_inherit = "car.property"

	def finish_sale(self):
		self._create_invoice()
		return super().finish_sale()

	def _create_invoice(self):
		journal = self.env["account.journal"].search([("type", "=", "sale")], limit = 1)
		for record in self:
			self.env["account.move"].create({
				"partner_id": record.buyer_id.id,
				"move_type": "out_invoice",
				"journal_id": journal.id,
                # Each property sold should be invoiced following certain conditions
				"invoice_line_ids": [
					(
						0,
						0,
						{
                            # Invoice at 6% of the selling price
							"name": record.name,
							"quantity": 1.0,
							"price_unit": record.selling_price * 6.0 / 100.0,
						},
					), (
						0,
						0,
						{
                            # Invoice with an additional 100.00 for administrative fees
							"name": "Administrative fees",
							"quantity": 1.0,
							"price_unit": 100.0,
						},
					),
				],
			})
		return True

#def inherited_action(self):
#    self.env["test_model"].create(
#        {
#            "name": "Test",
#            "line_ids": [
#                Command.create({
#                    "field_1": "value_1",
#                    "field_2": "value_2",
#                })
#            ],
#        }
#    )
#    return super().inherited_action()