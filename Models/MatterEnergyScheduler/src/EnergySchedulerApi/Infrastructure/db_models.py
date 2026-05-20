from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, JSON, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from .database import Base

class DmHousehold(Base):
    __tablename__ = "households"
    
    id = Column(String, primary_key=True, index=True)
    household_type = Column(String)
    location_latitude = Column(Float)
    location_longitude = Column(Float)
    pv_capacity_kw = Column(Float, default=0.0)
    bess_capacity_kwh = Column(Float, default=0.0)
    bess_min_soc_percent = Column(Float, default=20.0)
    bess_device_id = Column(String, nullable=True)
    bess_device_ip = Column(String, nullable=True)
    bess_device_port = Column(Integer, default=5540)
    bidding_zone = Column(String, nullable=True)
    
    appliances = relationship("DmAppliance", back_populates="household")

class DmAppliance(Base):
    __tablename__ = "appliances"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    power_usage_kw = Column(Float)
    duration_seconds = Column(Integer)
    deadline = Column(DateTime)
    matter_device_id = Column(String)
    matter_device_ip = Column(String)
    matter_device_port = Column(Integer, default=5540)
    matter_node_id = Column(Integer, nullable=True)
    device_type = Column(String, default="generic")
    household_id = Column(String, ForeignKey("households.id"), nullable=True)
    stored_fingerprint = Column(JSON, nullable=True) # Learned power profile [kW, kW, ...]
    
    household = relationship("DmHousehold", back_populates="appliances")
    schedules = relationship("DmSchedule", back_populates="appliance")

class DmMatterDevice(Base):
    __tablename__ = "matter_devices"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    matter_device_id = Column(String)
    ip_address = Column(String)
    port = Column(Integer, default=5540)
    device_type = Column(String)
    command_path = Column(String, default="/matter/command")
    status_path = Column(String, default="/matter/status")
    
    # Matter protocol credentials
    node_id = Column(Integer, nullable=True)
    fabric_id = Column(Integer, nullable=True)
    vendor_id = Column(Integer, nullable=True)
    product_id = Column(Integer, nullable=True)
    commissioning_date = Column(String, nullable=True)
    operational_credentials = Column(JSON, nullable=True)
    
    # Commissioning information
    setup_code = Column(String, nullable=True)
    discriminator = Column(Integer, nullable=True)
    commissioning_passcode = Column(Integer, nullable=True)

class DmSchedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    appliance_id = Column(String, ForeignKey("appliances.id"))
    start_time = Column(DateTime)
    duration_seconds = Column(Integer)
    power_usage_kw = Column(Float)
    status = Column(String, default="pending") # pending, running, completed, failed
    job_id = Column(String, nullable=True)
    is_daily = Column(Boolean, default=False)
    
    appliance = relationship("DmAppliance", back_populates="schedules")

class DmEnergyPrice(Base):
    __tablename__ = "energy_prices"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    bidding_zone = Column(String, index=True)
    start_time = Column(DateTime, index=True)
    price_per_kwh = Column(Float)
    is_real = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.now)
