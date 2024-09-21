from typing import Literal, List, Any, Optional
from datetime import datetime, date
import datetime as dt

from pydantic import HttpUrl

from rhinox.models.no_extra import NoExtraModel

T_CreditCard = Literal["CREDITO", "DEBITO"]
T_CategoriaProductos = Literal[
    "Promos",
    "EMPANADAS",
    "BEBIDAS",      # FIXME: Duplicado o tipeado manual?
    "Bebidas",      # FIXME: Duplicado o tipeado manual?
    "Frescas",
    "Extras",
    "Postres"
]


class Negocio(NoExtraModel):
    id: int
    nombre: str
    whatsapp_number: Optional[Any]
    categoria: int
    programa_pedidos: int
    controla_zona: int
    precio_entrega: int
    ciudad: str                 # FIXME: Mal tipeado, es string libre?
    direccion_sucursal: str
    commerce_id_plexo: int
    instagram_url: Optional[HttpUrl] = None


class Identidad(NoExtraModel):
    logo_url: HttpUrl
    favicon_url: HttpUrl
    banner_url: HttpUrl
    banner_mobile_url: HttpUrl
    color_primario: str
    color_secundario: str
    color_fondo: Optional[Any]
    color_font: Optional[Any]
    propina_habilitada: int


class MetodoPago(NoExtraModel):
    id: int
    nombre: str


class PopUp(NoExtraModel):
    descripcion: str
    promocion_imagen_url: HttpUrl


class Sucursal(NoExtraModel):
    id: int
    nombre: str
    ciudad: str
    direccion: str
    phone: str
    whatsapp: Optional[str]
    monto_minimo: int
    sucursal_imagen_url: HttpUrl
    tiempo_entrega: str             # TODO: Tiene formato de minutos, mejorar.
    tiempo_entrega_takeaway: str    # TODO: Tiene formato de minutos, mejorar.
    habilitado: int
    delivery_habilitado: int
    take_away_habilitado: int
    tiempo_espera_texto: str
    metodos_pago: List[MetodoPago]
    pop_ups: List[PopUp]


class Banco(NoExtraModel):
    id: int
    nombre: Literal["ITAU"]
    codigo: None
    icono: None


class PromoBanco(NoExtraModel):
    precio: float
    porcentaje: int
    banco: Banco


class PreciosDescuento(NoExtraModel):
    descripcion: str
    tipo: T_CreditCard
    precio_descuento: int


class CategoriaProductos(NoExtraModel):
    id: int
    negocio: int
    sucursal: None
    nombre: str
    categoria: T_CategoriaProductos
    imagenUrl: HttpUrl
    descripcion: str
    precio: float
    precio_informativo: Optional[int]
    updated_at: datetime
    created_at: datetime
    habilitado: int
    prioridad: int
    stock: Optional[int]
    stock_min: Optional[int]
    control_stock: int
    peso: int
    sku: None
    marca: None
    tiene_opcionales: int
    es_regalo: int
    giftcard: None
    monto_descuento: float
    promo_banco: Optional[PromoBanco] = None
    precios_descuento: Optional[List[PreciosDescuento]] = None
    precio_venta: Optional[int] = None


class Categorias(NoExtraModel):
    id: int
    nombre: str
    productos: List[CategoriaProductos]


class HorarioDetail(NoExtraModel):
    hora_inicio: dt.time
    hora_fin: dt.time
    acepta_delivery: int
    acepta_takeaway: int


class Horarios(NoExtraModel):
    Lunes: List[HorarioDetail]
    Martes: List[HorarioDetail]
    Miercoles: List[HorarioDetail]
    Jueves: List[HorarioDetail]
    Viernes: List[HorarioDetail]
    Sabado: List[HorarioDetail]
    Domingo: List[HorarioDetail]


class Descuento(NoExtraModel):
    descuento_id: int
    nombre: str
    fecha_inicio: date
    fecha_fin: date
    monto_minimo: int
    tipo_descuento: Literal[None, "PORCENTAJE"] = None
    valor: Optional[int] = None


class DescuentoMiniapp(NoExtraModel):
    nombre: Optional[str] = None
    tipo: T_CreditCard
    porcentaje: int
    fecha_inicio: date
    fecha_fin: date
    monto_minimo: int
    descripcion: Optional[str] = None


class Menu(NoExtraModel):
    status: Literal["success"]
    message: str
    code: Literal[200]
    abierto: bool
    acepta_delivery: bool
    acepta_takeaway: bool
    negocio: Negocio
    identidad: Identidad
    integraciones: list         # TODO: Ver si puede contener algún objeto dentro.
    sucursales: List[Sucursal]
    categorias: List[Categorias]
    total_categorias: int
    horarios: List[Horarios]
    descuento: Descuento
    descuento_miniapps: List[DescuentoMiniapp]

    def to_short_json(self) -> List[dict]:
        menu_short = []
        for cat in self.categorias:
            for p in cat.productos:
                prod_json = {
                    "product_id": p.id,
                    "name": p.nombre,
                    "category": p.categoria,
                    "description": p.descripcion,
                    "price": p.precio
                }
                #prod_json["promo_banco"] = p.promo_banco                   # TODO: Preguntar q onda esto.
                #prod_json["precios_descuento"] = p.precios_descuento       # TODO: Preguntar q onda esto.
                # TODO: promo_banco
                # TODO: precios_descuento
                # TODO: precio_venta
                menu_short.append(prod_json)
        return menu_short
