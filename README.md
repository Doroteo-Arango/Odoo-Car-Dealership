# Odoo-Car-Dealership
# Odoo Car Dealership Hub Module
Odoo is an open-source business management software suite that includes a wide range of applications for various business needs:
- Customer-relational management (CRM)
- Ecommerce
- Project Management
- Point of Sale (PoS)
- Inventory management 
- Accounting

Odoo provides a framework for developers to customize and extend its functionality to meet specific business requirements. Odoo manages databases using PostgreSQL, a free and open-source relational database management system emphasizing extensibility and SQL compliance.

## Table of Contents
1. [Introduction](#introduction)
2. [Car Dealer Module](#car-dealer-module)
3. [Prerequisites](#prerequisites)
4. [Conclusion](#conclusion)

## Introduction
This module was created with great inspiration from the estate property portfolio manager module created during the Odoo tutorial. This Odoo app manages car dealership assets, in detail, different types of cars. PostgreSQL is used for database management. This repository is designed to provide insights into the Odoo development framework, serving as a beginner-friendly entrance into Odoo development.

## Car Dealer Module
This module is focused on managing vehicular assets, which is a specific business area not covered by the standard Odoo modules. Therefore it was necessary to create our own new module to serve this purpose.

### Main Features
- **List View:** The module includes a list view that displays vehicle advertisements.
- **Form View:** The form view summarizes important property information, including the vehicle name, vehicle type, fuel type, seat availability and more.
- **Tabs:** There are two tabs on the form view:
  - The first tab contains details such as the number of seats, e.t.c.
  - The second tab lists offers for the current vehicle, including the ability for potential buyers to make offers above or below the expected selling price. Sellers can accept offers.
- User-interface: Using the Odoo "Website" pre-installed module, it was possible to create a sample website for use as a possible candidate for a user-friendly approach to the car salesman business.

## Prerequisites

- General Python framework knowledges (directory structure, routing, database integration, authentication e.t.c.) 
- Knowledge of Python for data models & scripting.
- Database & user management with PostgreSQL.
- UI development knowledge using HTML.

## Conclusion
By building projects in Odoo, one can build their own expertise of Python frameworks. This specific module can be a valuable asset for managing business assets in your business.
