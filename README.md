# Control de Costos

Aplicación de Streamlit para que un negocio pequeño tenga sus costos "a la mano": insumos, gastos operativos, productos, herramientas (con depreciación), ventas y punto de equilibrio.

## Requisitos

- **Python 3.12+**
- **uv** (recomendado) o `pip` + `venv`

## Instalación

### Opción A — uv (recomendado)

```bash
git clone https://github.com/Wooz27/banderillas_clase.git
cd banderillas_clase

uv venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### Opción B — pip

```bash
git clone https://github.com/Wooz27/banderillas_clase.git
cd banderillas_clase

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar

```bash
streamlit run main.py
```

Se abrirá en `http://localhost:8501`.

## Pantallas

- **Insumos** — precio, rinde (en productos), merma (%) y costo por unidad. "Sirve para" marca qué sabores usan cada insumo.
- **Gastos** — costos operativos; tipo Fijo/Variable y unidad Hora/Día/Mes. Con supuestos configurables (días/mes, horas/día).
- **Productos** — sabores y su precio de venta.
- **Herramientas** — costo, vida útil, valor de rescate y fecha de compra; calcula depreciación mensual y valor en libros.
- **Ventas** — registro de ventas por sabor (fecha, sabor, cantidad).
- **Análisis de ventas** — últimos 7/30/90 días: unidades, ingresos, margen y comparación contra el punto de equilibrio.
- **Punto de equilibrio** — `Q* = Costos fijos ÷ (Precio − Costo variable unitario)`.

## Cómo se calculan los costos

- Rinde neto: `rinde × (1 − merma/100)`
- Costo por unidad de insumo: `precio ÷ rinde neto`
- Costo variable de un sabor: suma de los insumos marcados con ese sabor
- Costo mensual de un gasto: `(monto ÷ cantidad) × factor`, con factor Hora = días×horas, Día = días, Mes = 1
- Depreciación mensual: `(costo − valor de rescate) ÷ (vida útil en años × 12)`
- Punto de equilibrio: `costos fijos ÷ margen de contribución`
- Análisis de ventas: margen real `= Σ cantidad × (precio − costo variable)` comparado contra los costos fijos del periodo

## Base de datos

Usa **SQLite** (`costos.db`) vía SQLAlchemy. El archivo **se crea automáticamente** al iniciar (`init_db()`), junto con las tablas y las columnas nuevas (migración aditiva). No se versiona en el repositorio.

## Librerías

- **streamlit** — interfaz web y tablas editables
- **SQLAlchemy** — ORM y SQLite
- **pandas** — DataFrames y cálculos
- **plotly** — gráficas
- **streamlit-option-menu** — navegación lateral
- **streamlit-extras** — tarjetas de métricas

Instaladas desde `requirements.txt`.
