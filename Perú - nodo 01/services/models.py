from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Text, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    fecha_registro = Column(TIMESTAMP, default=datetime.datetime.now)

    entradas = relationship("Entrada", back_populates="usuario")  

class Evento(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True)
    nombre_evento = Column(String(150), nullable=False)
    descripcion = Column(Text)
    fecha_evento = Column(Date, nullable=False)
    lugar = Column(String(150))
    precio = Column(DECIMAL(10,2), nullable=False)
    aforo = Column(Integer, nullable=False)

    entradas = relationship("Entrada", back_populates="evento")  

class Entrada(Base):
    __tablename__ = "entradas"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id", ondelete="CASCADE"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    total_pagado = Column(DECIMAL(10,2), nullable=False)
    fecha_compra = Column(TIMESTAMP, default=datetime.datetime.now)

    usuario = relationship("Usuario", back_populates="entradas")
    evento = relationship("Evento", back_populates="entradas")
