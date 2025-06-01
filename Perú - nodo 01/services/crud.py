from .models import Usuario, Evento, Entrada
from database import SessionLocal

def crear_usuario(nombre, email):
    session = SessionLocal()
    try:
        usuario = Usuario(nombre=nombre, email=email)
        session.add(usuario)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def listar_usuarios():
    session = SessionLocal()
    usuarios = session.query(Usuario).all()
    session.close()
    return usuarios

def crear_evento(nombre_evento, descripcion, fecha_evento, lugar, precio, aforo):
    session = SessionLocal()
    try:
        evento = Evento(
            nombre_evento=nombre_evento,
            descripcion=descripcion,
            fecha_evento=fecha_evento,
            lugar=lugar,
            precio=precio,
            aforo=aforo
        )
        session.add(evento)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def listar_eventos():
    session = SessionLocal()
    eventos = session.query(Evento).all()
    session.close()
    return eventos

def obtener_evento_por_nombre(nombre_evento):
    session = SessionLocal()
    evento = session.query(Evento).filter(Evento.nombre_evento == nombre_evento).first()
    session.close()
    return evento

def comprar_entradas(usuario_id, evento_id, cantidad):
    session = SessionLocal()
    try:
        evento = session.query(Evento).filter(Evento.id == evento_id).first()
        if not evento:
            raise Exception("Evento no encontrado")
        if cantidad <= 0:
            raise Exception("Cantidad inválida")
        total = evento.precio * cantidad

        entrada = Entrada(
            usuario_id=usuario_id,
            evento_id=evento_id,
            cantidad=cantidad,
            total_pagado=total
        )
        session.add(entrada)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
