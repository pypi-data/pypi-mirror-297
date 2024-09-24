from flask_crud.manage import CrudRegistrable
from flask_crud.view import FormView

class VehiculoViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "vehiculo"
    def __init__(self, matricula="", marca="", modelo="", color="", precio_de_venta=9.76) -> None:
        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.color = color
        self.precio_de_venta = precio_de_venta

    def __str__(self) -> str:
        return f"{self.matricula} | {self.marca} | {self.modelo} | {self.color}"

    @staticmethod
    def all():
        vehiculos = [
            VehiculoViewCfg("MAS-1223", "KIA", "FT 4x4", "Gris Neon", 100000),
            VehiculoViewCfg("SAS-726", "FORD", "Ford 150", "Rojo Metal", 500600),
        ]
        return vehiculos
    
class VehiculoCompradoViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "vehiculo"
    def __init__(self, matricula="", marca="", modelo="", color="") -> None:
        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.color = color

    def __str__(self) -> str:
        return f"{self.matricula} | {self.marca} | {self.modelo} | {self.color}"

    @staticmethod
    def all():
        vehiculos = [
            VehiculoViewCfg("MAS-1223", "KIA", "FT 4x4", "Gris Neon", 100000),
            VehiculoViewCfg("SAS-726", "FORD", "Ford 150", "Rojo Metal", 500600),
        ]
        return vehiculos


class ClienteViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "ClienteViewCfg"
    requireds = "numero_de_cedula,nombres,apellidos,dirección,ciudad,telefono".split(",")
    # disableds = "numero_de_cedula,nombres,apellidos,dirección,ciudad,telefono".split(",")
    enums = {
        "ciudad": ["PORTOVIEJO", "MANTA", "CHONE"],
        "vehiculos": VehiculoViewCfg.all(),
    }
    def __init__(self, numero_de_cedula="1301347618", nombres="", apellidos="", dirección="", ciudad="SELECCIONE:", telefono="0998826188", vehiculos="SELECCIONE:") -> None:
        self.numero_de_cedula = numero_de_cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.dirección = dirección
        self.ciudad = ciudad
        self.telefono = telefono
        self.vehiculos = vehiculos

class ClienteConsultaViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "ClienteConsultaViewCfg"
    requireds = ["numero_de_cedula"]
    # disableds = "numero_de_cedula,nombres,apellidos,dirección,ciudad,telefono".split(",")
    def __init__(self, numero_de_cedula="1301347618") -> None:
        self.numero_de_cedula = numero_de_cedula

class MantenimientoEliminacionViewCfg(CrudRegistrable):
    id_name = "id"
    entity_name = "MantenimientoEliminacionViewCfg"
    requireds = ["matrícula"]
    # disableds = "numero_de_cedula,nombres,apellidos,dirección,ciudad,telefono".split(",")
    def __init__(self, matrícula="1301347618", motivo="\n") -> None:
        self.matrícula = matrícula
        self.motivo = motivo

class RevisionViewCfg(CrudRegistrable):
    table_name = "revisiones"           # Nombre de la tabla en la base de datos
    id_name = "id"            # Nombre de la columna del ID en la tabla
    entity_name = "revision"           # Nombre de la entidad para uso en la lógica de negocio    
    enums = {
        "tipo_mantenimiento":["cambio de frenos", "cambio de aceite", "cambio de filtro"]
    }

    def __init__(self, fecha_hora_recepcion="2024-09-22 14:30", fecha_hora_entrega="2024-09-22 14:30", tipo_mantenimiento="SELECCIONE:") -> None:
        self.fecha_hora_recepcion = fecha_hora_recepcion
        self.fecha_hora_entrega = fecha_hora_entrega
        self.tipo_mantenimiento = tipo_mantenimiento
            
