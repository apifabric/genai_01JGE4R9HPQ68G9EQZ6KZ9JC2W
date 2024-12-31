# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Customer(Base):
    """description: Model representing a customer in the CRM system."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address_id = Column(Integer, ForeignKey('address.id'))

class Address(Base):
    """description: Model representing a physical address in the CRM system."""
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

class Order(Base):
    """description: Model representing an order made by a customer."""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_date = Column(DateTime)
    shipped_date = Column(DateTime)
    customer_id = Column(Integer, ForeignKey('customer.id'))

class Product(Base):
    """description: Model representing a product sold by the CRM system."""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

class OrderItem(Base):
    """description: Model representing an item in an order, linking orders to products."""
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)

class Employee(Base):
    """description: Model representing an employee in the CRM system who takes or manages orders."""
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)

class CustomerType(Base):
    """description: Model representing a customer type or category."""
    __tablename__ = 'customer_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)

class CustomerCustomerType(Base):
    """description: Junction table for many-to-many relationship between customers and customer types."""
    __tablename__ = 'customer_customer_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer_type_id = Column(Integer, ForeignKey('customer_type.id'))

class EmployeeOrder(Base):
    """description: Junction table for many-to-many relationship between employees and orders."""
    __tablename__ = 'employee_order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    order_id = Column(Integer, ForeignKey('order.id'))

class Supplier(Base):
    """description: Model representing a supplier of products."""
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

class ProductSupplier(Base):
    """description: Link table mapping products to their suppliers."""
    __tablename__ = 'product_supplier'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'))
    supplier_id = Column(Integer, ForeignKey('supplier.id'))

class Review(Base):
    """description: Model representing a review made by a customer for a product."""
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    review_text = Column(String)
    rating = Column(Integer)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    customer1 = Customer(name="John Doe", email="john@example.com", phone="1234567890", address_id=1)
    customer2 = Customer(name="Jane Smith", email="jane@example.com", phone="0987654321", address_id=2)
    order1 = Order(order_date=date(2023, 1, 15), shipped_date=date(2023, 1, 18), customer_id=1)
    order2 = Order(order_date=date(2023, 2, 1), shipped_date=date(2023, 2, 4), customer_id=2)
    product1 = Product(name="Widget", description="A useful widget", price=9.99)
    product2 = Product(name="Gadget", description="An advanced gadget", price=23.45)
    orderitem1 = OrderItem(order_id=1, product_id=1, quantity=2, unit_price=9.99)
    orderitem2 = OrderItem(order_id=2, product_id=2, quantity=1, unit_price=23.45)
    employee1 = Employee(first_name="Alice", last_name="Brown", email="alice.brown@example.com", phone="2223334444")
    employee2 = Employee(first_name="Bob", last_name="Green", email="bob.green@example.com", phone="5556667777")
    supplier1 = Supplier(name="SupplyCo", email="contact@supplyco.com", phone="1112223333")
    supplier2 = Supplier(name="GoodsRUs", email="sales@goodsrus.com", phone="8889990000")
    review1 = Review(customer_id=1, product_id=1, review_text="Excellent product!", rating=5)
    review2 = Review(customer_id=2, product_id=2, review_text="Good value", rating=4)
    
    
    
    session.add_all([customer1, customer2, order1, order2, product1, product2, orderitem1, orderitem2, employee1, employee2, supplier1, supplier2, review1, review2])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
