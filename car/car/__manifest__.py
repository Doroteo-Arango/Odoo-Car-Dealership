{
    "name": "Car Dealership",  # The name that will appear in the App list
    "version": "16.0",  # Version
    "application": True,  # This line says the module is an App, and not a module
    "depends": ["base"],  # dependencies
    "data": [
        # Data security file
        'security/ir.model.access.csv',
        # Rest of UI files
        'views/dealership_cars_type_views.xml',
        'views/dealership_cars_tag_views.xml',
        'views/dealership_cars_offer_views.xml',
        'views/res_user_views.xml',
        'views/dealership_cars_views.xml',
        'views/car_menus.xml',
    ],
    "installable": True,
    'license': 'LGPL-3',
}