+-------------------------+
|        Cliente          |
| (Browser / Postman)     |
+-----------+-------------+
            |
            | 1. GET /info
            | 2. POST /mensaje
            v
+-------------------------+
|      Servidor Flask     |
|  - /info (GET)          |
|  - /mensaje (POST)      |
+-----------+-------------+
            |
            | Guarda mensaje
            v
+-------------------------+
|      Base de Datos      |
|   (ej. SQLite o MySQL)  |
+-------------------------+
