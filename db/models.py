from datetime import date

from sqlalchemy import Date, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from utils.costos import costo_unitario, por_unidad

TIPO_PRODUCCION = "producción"
TIPOS_GASTO = ("Fijo", "Variable")


class Insumo(Base):
    __tablename__ = "insumos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[str] = mapped_column(String(20))
    rinde: Mapped[float | None] = mapped_column(Float, nullable=True)
    mermas: Mapped[float | None] = mapped_column(Float, nullable=True, default=0.0)
    precio: Mapped[float] = mapped_column(Float, default=0.0)
    sirve_para: Mapped[str] = mapped_column(String, default="")

    @property
    def costo_unitario(self) -> float | None:
        if self.tipo != TIPO_PRODUCCION:
            return None
        return costo_unitario(self.precio, self.rinde or 0.0, self.mermas or 0.0)


class Gasto(Base):
    __tablename__ = "gastos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    tipo: Mapped[str] = mapped_column(String(20), default=TIPOS_GASTO[0])
    monto: Mapped[float] = mapped_column(Float, default=0.0)
    unidad: Mapped[str] = mapped_column(String(10), default="Mes")
    cantidad: Mapped[float] = mapped_column(Float, default=1.0)

    @property
    def costo_unitario(self) -> float:
        return por_unidad(self.monto, self.cantidad)


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    precio: Mapped[float] = mapped_column(Float, default=0.0)


class Herramienta(Base):
    __tablename__ = "herramientas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    fecha_compra: Mapped[date | None] = mapped_column(Date, nullable=True)
    costo: Mapped[float] = mapped_column(Float, default=0.0)
    vida_util: Mapped[float] = mapped_column(Float, default=0.0)
    valor_rescate: Mapped[float] = mapped_column(Float, default=0.0)


class Venta(Base):
    __tablename__ = "ventas"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[date | None] = mapped_column(Date, nullable=True)
    sabor: Mapped[str] = mapped_column(String(100))
    cantidad: Mapped[float] = mapped_column(Float, default=0.0)
