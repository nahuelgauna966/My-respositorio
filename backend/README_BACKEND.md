# CafecitoApp — Backend

> **Sistema de Administración de Cafetería**
> Grupo 1 | Programación II | 2026

API REST construida con **FastAPI + PostgreSQL**, siguiendo arquitectura en capas (Routes → Services → Models) con autenticación JWT y validación de datos mediante Pydantic.

---

## Índice

1. [Tecnologías](#tecnologías)
2. [Estructura del proyecto](#estructura-del-proyecto)
3. [Configuración e instalación](#configuración-e-instalación)
4. [Cómo correr el proyecto](#cómo-correr-el-proyecto)
5. [Variables de entorno](#variables-de-entorno)
6. [Arquitectura — explicación por capas](#arquitectura--explicación-por-capas)
7. [Modelos de base de datos](#modelos-de-base-de-datos)
8. [Endpoints disponibles](#endpoints-disponibles)
9. [Cómo probar la API](#cómo-probar-la-api)
10. [Estado del proyecto por Sprint](#estado-del-proyecto-por-sprint)
11. [Próximos pasos](#próximos-pasos)

---

## Tecnologías

| Tecnología | Versión | Para qué se usa |
|---|---|---|
| Python | 3.11 | Lenguaje base |
| FastAPI | 0.136+ | Framework web asíncrono |
| SQLAlchemy | 2.0+ | ORM — mapeo de objetos a tablas |
| asyncpg | 0.31+ | Driver asíncrono de PostgreSQL |
| Pydantic | 2.x | Validación de datos y schemas |
| pydantic-settings | 2.x | Lectura de variables de entorno |
| passlib + bcrypt | — | Encriptación de contraseñas |
| python-jose | — | Generación y validación de JWT |
| alembic | 1.x | Migraciones de base de datos |
| uvicorn | 0.48+ | Servidor ASGI para correr FastAPI |
| uv | — | Gestor de dependencias y entorno virtual |

---

## Estructura del proyecto

```
backend/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Lee variables del .env con pydantic-settings
│   │   └── database.py        # Motor async, sesiones y clase Base de SQLAlchemy
│   │
│   ├── models/
│   │   ├── __init__.py        # Importa todos los modelos (necesario para Alembic)
│   │   ├── usuario.py         # Tabla usuarios
│   │   ├── categoria.py       # Tabla categorias
│   │   ├── producto.py        # Tabla productos
│   │   ├── mesa.py            # Tabla mesas
│   │   ├── pedido.py          # Tabla pedidos
│   │   ├── detalle_pedido.py  # Tabla detalle_pedidos (items de cada pedido)
│   │   ├── pago.py            # Tabla pagos
│   │   └── caja.py            # Tabla cajas
│   │
│   ├── schemas/
│   │   ├── usuario.py         # UsuarioCreate, UsuarioResponse, LoginRequest, TokenResponse
│   │   ├── categoria.py       # CategoriaCreate, CategoriaResponse
│   │   ├── producto.py        # ProductoCreate, ProductoUpdate, ProductoResponse
│   │   ├── mesa.py            # MesaCreate, MesaUpdate, MesaResponse
│   │   ├── pedido.py          # PedidoCreate, PedidoUpdate, PedidoResponse, DetallePedidoCreate
│   │   ├── pago.py            # PagoCreate, PagoResponse
│   │   └── caja.py            # CajaApertura, CajaCierre, CajaResponse
│   │
│   ├── services/
│   │   ├── auth_service.py    # Login, hash/verify password, create JWT, crear usuario
│   │   ├── mesa_service.py    # CRUD de mesas
│   │   ├── producto_service.py# CRUD de productos
│   │   ├── pedido_service.py  # Crear pedido, calcular total, cambiar estado de mesa
│   │   └── caja_service.py    # Apertura y cierre de caja
│   │
│   └── routes/
│       ├── __init__.py        # Router principal /api/v1 que agrupa todos los routers
│       ├── auth.py            # POST /auth/login, POST /auth/register, GET /auth/me
│       ├── mesas.py           # GET/POST /mesas, GET/PATCH /mesas/{id}
│       ├── productos.py       # GET/POST /productos, GET/PATCH/DELETE /productos/{id}
│       ├── pedidos.py         # GET/POST /pedidos, GET/PATCH /pedidos/{id}
│       └── caja.py            # GET /caja, POST /caja/apertura, POST /caja/cierre
│
├── main.py                    # Punto de entrada — app FastAPI, CORS, lifespan, router
├── .env                       # Variables de entorno (NO subir a GitHub)
├── .python-version            # Python 3.11
├── pyproject.toml             # Dependencias del proyecto (gestionadas con uv)
└── uv.lock                    # Lock file de dependencias
```

---

## Configuración e instalación

### Requisitos previos

- Python 3.11
- PostgreSQL corriendo localmente
- `uv` instalado

#### Instalar uv (si no lo tenés)

```powershell
# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Pasos de instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/SoftwareSegundo2026/grupo1.git
cd grupo1/backend

# 2. Instalar dependencias (crea el .venv automáticamente)
uv sync

# 3. Crear la base de datos en PostgreSQL
psql -U postgres -c "CREATE DATABASE cafecito_db;"

# 4. Crear el archivo .env (ver sección Variables de entorno)
cp .env.example .env  # o crearlo manualmente
```

---

## Cómo correr el proyecto

```bash
# Desde la carpeta /backend
uv run uvicorn main:app --reload
```

El servidor levanta en: `http://127.0.0.1:8000`

> `--reload` hace que el servidor se reinicie automáticamente cada vez que guardás un archivo. Solo usar en desarrollo.

### Verificar que funciona

```bash
# Respuesta esperada: {"message": "CafecitoApp API funcionando", "version": "1.0.0"}
curl http://localhost:8000/
```

---

## Variables de entorno

Crear un archivo `.env` en la carpeta `/backend` con el siguiente contenido:

```env
DATABASE_URL=postgresql+asyncpg://postgres:TU_CONTRASEÑA@localhost:5432/cafecito_db
SECRET_KEY=cafecito_secret_key_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
```

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DATABASE_URL` | Cadena de conexión a PostgreSQL | `postgresql+asyncpg://postgres:1234@localhost:5432/cafecito_db` |
| `SECRET_KEY` | Clave secreta para firmar tokens JWT | Cualquier string largo y aleatorio |
| `ALGORITHM` | Algoritmo de codificación del JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Duración de la sesión en minutos | `480` (8 horas = 1 turno laboral) |

> **Importante:** El archivo `.env` nunca se sube a GitHub. Está en el `.gitignore`.

---

## Arquitectura — explicación por capas

El backend sigue una arquitectura en capas donde cada capa tiene una única responsabilidad.

```
Request HTTP
     ↓
  ROUTES          → Recibe el request, valida con schemas, devuelve respuesta
     ↓
  SERVICES        → Contiene toda la lógica de negocio
     ↓
  MODELS          → Representa las tablas de la base de datos
     ↓
  DATABASE        → PostgreSQL
```

### ¿Por qué esta separación?

**Routes** solo saben recibir y responder. No tienen lógica.

**Services** contienen la lógica. Por ejemplo, cuando se crea un pedido, el service:
1. Verifica que cada producto existe
2. Calcula el subtotal por ítem
3. Calcula el total del pedido
4. Cambia el estado de la mesa a "ocupada"

Todo eso vive en el service, no en el route. Si mañana necesitás esa misma lógica desde otro endpoint, simplemente llamás al mismo service.

**Models** son clases Python que SQLAlchemy traduce a tablas SQL. Definen columnas, tipos de datos y relaciones entre tablas.

**Schemas** (Pydantic) son diferentes a los modelos. Definen qué datos entran y qué datos salen por la API. Ejemplo: el modelo `Usuario` tiene `password_hash`, pero el schema `UsuarioResponse` nunca lo incluye — protege los datos sensibles.

---

## Modelos de base de datos

### Diagrama de relaciones

```
categorias
    ↑ (1 categoría tiene muchos productos)
productos ←── detalle_pedidos ──→ pedidos ──→ mesas
                                      ↓           ↑
                                    pagos      usuarios
cajas (independiente)
```

### Descripción de cada tabla

#### `usuarios`
| Columna | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| nombre | String(100) | Nombre completo |
| email | String(150) unique | Email — usado para login |
| password_hash | String(255) | Contraseña encriptada con bcrypt |
| rol | String(20) | `admin` o `mozo` |
| activo | Boolean | Si el usuario puede acceder al sistema |

#### `mesas`
| Columna | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| numero | Integer unique | Número visible de la mesa |
| estado | String(30) | `libre`, `ocupada`, `reservada`, `pendiente_cobro`, `en_limpieza` |

#### `pedidos`
| Columna | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| mesa_id | FK → mesas | Mesa asociada al pedido |
| usuario_id | FK → usuarios | Mozo que tomó el pedido |
| estado | String(30) | `pendiente`, `en_preparacion`, `listo`, `entregado`, `pagado`, `cancelado` |
| total | Numeric(10,2) | Total calculado automáticamente |
| fecha | DateTime | Fecha y hora de creación |

#### `detalle_pedidos`
| Columna | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| pedido_id | FK → pedidos | Pedido al que pertenece |
| producto_id | FK → productos | Producto pedido |
| cantidad | Integer | Cantidad de unidades |
| subtotal | Numeric(10,2) | Precio al momento del pedido × cantidad |

> El subtotal se guarda al momento de crear el pedido para preservar el precio histórico aunque el producto cambie de precio después.

#### `productos`
| Columna | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| nombre | String(100) | Nombre del producto |
| descripcion | String(255) | Descripción opcional |
| precio | Numeric(10,2) | Precio unitario |
| stock | Integer | Cantidad disponible |
| disponible | Boolean | Si aparece en el menú |
| categoria_id | FK → categorias | Categoría del producto |

#### `pagos`
| Columna | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| pedido_id | FK → pedidos | Pedido que se está pagando |
| metodo_pago | String(30) | `efectivo`, `debito`, `credito`, `transferencia`, `mercado_pago` |
| monto | Numeric(10,2) | Monto abonado |
| fecha | DateTime | Fecha y hora del pago |

#### `cajas`
| Columna | Tipo | Descripción |
|---|---|---|
| id | Integer PK | Identificador único |
| fecha_apertura | DateTime | Cuándo se abrió |
| fecha_cierre | DateTime nullable | Cuándo se cerró |
| monto_inicial | Numeric(10,2) | Monto al abrir |
| monto_final | Numeric(10,2) nullable | Monto al cerrar |
| estado | String(20) | `abierta` o `cerrada` |

---

## Endpoints disponibles

Base URL: `http://localhost:8000/api/v1`

### Autenticación

| Método | Endpoint | Descripción | Auth requerida |
|---|---|---|---|
| POST | `/auth/login` | Iniciar sesión | No |
| POST | `/auth/register` | Crear usuario | No (Sprint 4: solo admin) |
| GET | `/auth/me` | Usuario autenticado | Sí (Sprint 4) |

**Ejemplo login:**
```json
POST /api/v1/auth/login
{
  "email": "admin@cafecito.com",
  "password": "123456"
}
```

**Respuesta:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "usuario": {
    "id": 1,
    "nombre": "Nahuel Gauna",
    "email": "admin@cafecito.com",
    "rol": "admin",
    "activo": true
  }
}
```

---

### Mesas

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/mesas/` | Listar todas las mesas |
| GET | `/mesas/{id}` | Obtener una mesa |
| POST | `/mesas/` | Crear mesa |
| PATCH | `/mesas/{id}` | Actualizar estado de mesa |

**Ejemplo crear mesa:**
```json
POST /api/v1/mesas/
{
  "numero": 1
}
```

**Ejemplo actualizar estado:**
```json
PATCH /api/v1/mesas/1
{
  "estado": "ocupada"
}
```

---

### Productos

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/productos/` | Listar todos los productos |
| GET | `/productos/{id}` | Obtener un producto |
| POST | `/productos/` | Crear producto |
| PATCH | `/productos/{id}` | Actualizar producto |
| DELETE | `/productos/{id}` | Eliminar producto |

**Ejemplo crear producto:**
```json
POST /api/v1/productos/
{
  "nombre": "Café con leche",
  "precio": 850.00,
  "stock": 100,
  "disponible": true,
  "categoria_id": 1
}
```

---

### Pedidos

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/pedidos/` | Listar pedidos activos |
| GET | `/pedidos/{id}` | Obtener un pedido |
| POST | `/pedidos/` | Crear pedido |
| PATCH | `/pedidos/{id}` | Actualizar estado del pedido |

**Ejemplo crear pedido:**
```json
POST /api/v1/pedidos/
{
  "mesa_id": 3,
  "detalles": [
    { "producto_id": 1, "cantidad": 2 },
    { "producto_id": 4, "cantidad": 1 }
  ]
}
```

> Al crear un pedido, el sistema automáticamente cambia el estado de la mesa a `ocupada` y calcula el total.

**Ejemplo cambiar estado:**
```json
PATCH /api/v1/pedidos/1
{
  "estado": "en_preparacion"
}
```

> Al cambiar el estado a `pagado`, el sistema automáticamente libera la mesa.

---

### Caja

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/caja/` | Estado de la caja actual |
| POST | `/caja/apertura` | Abrir caja |
| POST | `/caja/cierre` | Cerrar caja |

**Ejemplo abrir caja:**
```json
POST /api/v1/caja/apertura
{
  "monto_inicial": 5000.00
}
```

---

## Cómo probar la API

### Opción 1 — Swagger UI (recomendado)

Abrí en el navegador:
```
http://localhost:8000/docs
```

FastAPI genera automáticamente una interfaz visual donde podés probar todos los endpoints sin necesidad de herramientas externas. Podés ver los schemas de entrada/salida, ejecutar requests y ver las respuestas en tiempo real.

### Opción 2 — ReDoc

```
http://localhost:8000/redoc
```

Documentación alternativa en formato más legible, útil para compartir con el equipo.

### Opción 3 — curl

```bash
# Listar mesas
curl http://localhost:8000/api/v1/mesas/

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@cafecito.com","password":"123456"}'
```

### Datos de prueba — setup inicial

Para tener datos con qué trabajar, crear primero una categoría y un producto:

```bash
# 1. Crear categoría
curl -X POST http://localhost:8000/api/v1/productos/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Cafetería"}'

# 2. Crear usuario admin
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Admin","email":"admin@cafecito.com","password":"123456","rol":"admin"}'

# 3. Crear mesas
curl -X POST http://localhost:8000/api/v1/mesas/ \
  -H "Content-Type: application/json" \
  -d '{"numero": 1}'
```

---

## Estado del proyecto por Sprint

### ✅ Sprint 1 — Kick-off & Arquitectura (18/05 – 25/05)
- [x] Definición de tecnologías
- [x] Estructura inicial del proyecto
- [x] Contratos API definidos
- [x] Entidades principales identificadas
- [x] Roles de usuario definidos

### ✅ Sprint 2 — Modelos & Endpoints Core (26/05 – 01/06)
- [x] Instalación de dependencias con uv
- [x] Configuración de variables de entorno (`config.py`)
- [x] Conexión a PostgreSQL con SQLAlchemy async (`database.py`)
- [x] 8 modelos creados (Usuario, Categoria, Producto, Mesa, Pedido, DetallePedido, Pago, Caja)
- [x] 7 schemas Pydantic con separación Create/Update/Response
- [x] 5 services con lógica de negocio
- [x] 5 routers con endpoints core
- [x] CORS configurado para Next.js
- [x] Creación automática de tablas al iniciar la app
- [x] API corriendo y documentación disponible en `/docs`

### 🔜 Sprint 3 — Lógica de negocio / FE: componentes UI (02/06 – 08/06)
- [ ] Endpoints v1 conectados con frontend
- [ ] Lógica de negocio completa en services
- [ ] Componentes UI del frontend conectados a la API

### 🔜 Sprint 4 — Validaciones, Auth, Errores (09/06 – 15/06)
- [ ] Middleware JWT — protección de rutas por rol
- [ ] `GET /auth/me` funcional con token
- [ ] Validaciones de negocio (mesa ya ocupada, caja ya abierta, etc.)
- [ ] Manejo global de errores
- [ ] Pruebas unitarias BE

### 🔜 Sprint 5 — Optimización & Docs API (16/06 – 22/06)
- [ ] Optimización de queries
- [ ] Documentación completa de la API
- [ ] Feature freeze del backend

### 🔜 Sprint 6 — QA, Fixes, Despliegue Staging (23/06 – 29/06)
- [ ] QA del backend
- [ ] Corrección de bugs
- [ ] **Entrega BE — Lunes 29/06**

---

## Próximos pasos

El siguiente paso inmediato es el **Sprint 3**, donde el frontend va a consumir esta API por primera vez. Para prepararlo:

1. Agregar datos de prueba a la base de datos (categorías, productos, mesas)
2. Implementar el middleware JWT para proteger rutas
3. Conectar los primeros endpoints desde Next.js

---

## Equipo

| Nombre | Rol |
|---|---|
| Gauna Nahuel | Desarrollo |
| López Valentín | Desarrollo |
| Napoli Alexis | Desarrollo |

**Repositorio:** https://github.com/SoftwareSegundo2026/grupo1
**Gestor de proyecto:** https://cafecito.atlassian.net/jira/software/projects/CFB/boards/1
