# Desafio FIFA

# Desafío 1: FIFA ULTIMATE TEAM (Back-end)

Este proyecto implementa el back-end de una aplicación Django para gestionar un sistema de cartas de jugadores inspirado en FIFA Ultimate Team. La API permite la gestión (CRUD) de usuarios, cartas y la asignación y consulta de equipos.

## 👥 Autores

- Álvaro Martín
- Jose Enrique Águila

---

## 🚀 API Endpoints

A continuación se detallan todos los _endpoints_ implementados en la API.

### 👤 Gestión de Usuarios (Req1)

| Método   | URL                                          | Descripción                                    | Autor(es) |
| :------- | :------------------------------------------- | :--------------------------------------------- | :-------- |
| `GET`    | `/gestion/usuarios/`                         | Lista todos los usuarios registrados.          | _Alvaro_  |
| `GET`    | `/gestion/usuarios/<int:user_id>/`           | Obtiene los detalles de un usuario específico. | _Alvaro_  |
| `POST`   | `/gestion/usuarios/crear`                    | Crea un nuevo usuario.                         | _Alvaro_  |
| `PUT`    | `/gestion/usuarios/actualizar/<int:user_id>` | Actualiza los datos de un usuario.             | _Alvaro_  |
| `DELETE` | `/gestion/usuarios/borrar/<int:user_id>`     | Borra un usuario de la base de datos.          | _Alvaro_  |

### 🃏 Gestión de Cartas (Req2)

| Método   | URL                                    | Descripción                                               | Autor(es) |
| :------- | :------------------------------------- | :-------------------------------------------------------- | :-------- |
| `GET`    | `/gestion/cartas/`                     | Lista todas las cartas **activas**.                       | _Aguila_  |
| `GET`    | `/gestion/cartas/<int:id>/`            | Obtiene los detalles de una carta específica.             | _Aguila_  |
| `POST`   | `/gestion/cartas/crear/`               | Crea una nueva carta (Jugador o Portero).                 | _Aguila_  |
| `PUT`    | `/gestion/cartas/<int:id>/actualizar/` | Actualiza los datos de una carta.                         | _Aguila_  |
| `DELETE` | `/gestion/cartas/<int:id>/eliminar/`   | Realiza un **borrado lógico** de la carta (la desactiva). | _Aguila_  |

### 🏟️ Gestión de Equipos (Req3, Req6, Req7)

| Método   | URL                                               | Descripción                                                                 | Autor(es) |
| :------- | :------------------------------------------------ | :-------------------------------------------------------------------------- | :-------- |
| `POST`   | `/gestion/usuarios/<int:user_id>/asignar`         | Asigna un equipo aleatorio (23-25 jugadores) a un usuario que no tiene uno. | _Alvaro_  |
| `GET`    | `/gestion/usuarios/<int:user_id>/equipo/`         | Consulta el equipo de un usuario, mostrando solo cartas activas.            | _Alvaro_  |
| `POST`   | `/gestion/equipo/<int:equipo_id>/anadir-carta/`   | (Req7) Añade una carta específica a un equipo.                              | _Aguila_  |
| `DELETE` | `/gestion/equipo/<int:equipo_id>/eliminar-carta/` | (Opcional) Elimina una carta de un equipo.                                  | _Aguila_  |

---

## ⚙️ Comandos de Gestión (Req5)

Para poblar la base de datos, se han creado dos comandos:

- `python manage.py crear_usuarios`: Crea 30 usuarios de prueba.
- `python manage.py crear_cartas`: Crea 150 cartas de jugadores aleatorios (con posiciones ponderadas).

## 🧪 Pruebas (RA5)

El proyecto incluye una batería de tests (en `gestion/tests.py`) que cubren las siguientes funcionalidades:

- **Tests Unitarios** (Modelo `Usuario`).
- **Tests de Vistas (API)**:
  - CRUD completo de Usuarios (GET, GET por ID, POST, PUT, DELETE).
  - Test de `asignar_equipo` (POST), incluyendo la preparación de la BBDD de pruebas.
  - Test de `listar_equipo` (GET).
