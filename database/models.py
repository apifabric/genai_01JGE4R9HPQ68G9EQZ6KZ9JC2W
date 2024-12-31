# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 31, 2024 10:39:28
# Database: sqlite:////tmp/tmp.KT49Xfwynh-01JGE4R9HPQ68G9EQZ6KZ9JC2W/CRM_System/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

Base = SAFRSBaseX



class Address(Base):  # type: ignore
    """
    description: Model representing a physical address in the CRM system.
    """
    __tablename__ = 'address'
    _s_collection_name = 'Address'  # type: ignore

    id = Column(Integer, primary_key=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    CustomerList : Mapped[List["Customer"]] = relationship(back_populates="address")



class CustomerType(Base):  # type: ignore
    """
    description: Model representing a customer type or category.
    """
    __tablename__ = 'customer_type'
    _s_collection_name = 'CustomerType'  # type: ignore

    id = Column(Integer, primary_key=True)
    description = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    CustomerCustomerTypeList : Mapped[List["CustomerCustomerType"]] = relationship(back_populates="customer_type")



class Employee(Base):  # type: ignore
    """
    description: Model representing an employee in the CRM system who takes or manages orders.
    """
    __tablename__ = 'employee'
    _s_collection_name = 'Employee'  # type: ignore

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    EmployeeOrderList : Mapped[List["EmployeeOrder"]] = relationship(back_populates="employee")



class Product(Base):  # type: ignore
    """
    description: Model representing a product sold by the CRM system.
    """
    __tablename__ = 'product'
    _s_collection_name = 'Product'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductSupplierList : Mapped[List["ProductSupplier"]] = relationship(back_populates="product")
    ReviewList : Mapped[List["Review"]] = relationship(back_populates="product")
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="product")



class Supplier(Base):  # type: ignore
    """
    description: Model representing a supplier of products.
    """
    __tablename__ = 'supplier'
    _s_collection_name = 'Supplier'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductSupplierList : Mapped[List["ProductSupplier"]] = relationship(back_populates="supplier")



class Customer(Base):  # type: ignore
    """
    description: Model representing a customer in the CRM system.
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address_id = Column(ForeignKey('address.id'))

    # parent relationships (access parent)
    address : Mapped["Address"] = relationship(back_populates=("CustomerList"))

    # child relationships (access children)
    CustomerCustomerTypeList : Mapped[List["CustomerCustomerType"]] = relationship(back_populates="customer")
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")
    ReviewList : Mapped[List["Review"]] = relationship(back_populates="customer")



class ProductSupplier(Base):  # type: ignore
    """
    description: Link table mapping products to their suppliers.
    """
    __tablename__ = 'product_supplier'
    _s_collection_name = 'ProductSupplier'  # type: ignore

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('product.id'))
    supplier_id = Column(ForeignKey('supplier.id'))

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("ProductSupplierList"))
    supplier : Mapped["Supplier"] = relationship(back_populates=("ProductSupplierList"))

    # child relationships (access children)



class CustomerCustomerType(Base):  # type: ignore
    """
    description: Junction table for many-to-many relationship between customers and customer types.
    """
    __tablename__ = 'customer_customer_type'
    _s_collection_name = 'CustomerCustomerType'  # type: ignore

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    customer_type_id = Column(ForeignKey('customer_type.id'))

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("CustomerCustomerTypeList"))
    customer_type : Mapped["CustomerType"] = relationship(back_populates=("CustomerCustomerTypeList"))

    # child relationships (access children)



class Order(Base):  # type: ignore
    """
    description: Model representing an order made by a customer.
    """
    __tablename__ = 'order'
    _s_collection_name = 'Order'  # type: ignore

    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime)
    shipped_date = Column(DateTime)
    customer_id = Column(ForeignKey('customer.id'))

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    EmployeeOrderList : Mapped[List["EmployeeOrder"]] = relationship(back_populates="order")
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="order")



class Review(Base):  # type: ignore
    """
    description: Model representing a review made by a customer for a product.
    """
    __tablename__ = 'review'
    _s_collection_name = 'Review'  # type: ignore

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    product_id = Column(ForeignKey('product.id'))
    review_text = Column(String)
    rating = Column(Integer)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("ReviewList"))
    product : Mapped["Product"] = relationship(back_populates=("ReviewList"))

    # child relationships (access children)



class EmployeeOrder(Base):  # type: ignore
    """
    description: Junction table for many-to-many relationship between employees and orders.
    """
    __tablename__ = 'employee_order'
    _s_collection_name = 'EmployeeOrder'  # type: ignore

    id = Column(Integer, primary_key=True)
    employee_id = Column(ForeignKey('employee.id'))
    order_id = Column(ForeignKey('order.id'))

    # parent relationships (access parent)
    employee : Mapped["Employee"] = relationship(back_populates=("EmployeeOrderList"))
    order : Mapped["Order"] = relationship(back_populates=("EmployeeOrderList"))

    # child relationships (access children)



class OrderItem(Base):  # type: ignore
    """
    description: Model representing an item in an order, linking orders to products.
    """
    __tablename__ = 'order_item'
    _s_collection_name = 'OrderItem'  # type: ignore

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'))
    product_id = Column(ForeignKey('product.id'))
    quantity = Column(Integer)
    unit_price = Column(Float)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderItemList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderItemList"))

    # child relationships (access children)
