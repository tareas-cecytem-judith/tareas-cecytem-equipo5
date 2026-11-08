# TareasCECyTEM

Aplicación Flask + MySQL para practicar el ciclo completo de despliegue:
**XAMPP → Aiven → GitHub → Render**.

## Estructura

```
tareas-cecytem/
├── app.py              # rutas de la aplicación (INSERT, UPDATE, DELETE, /salud)
├── db.py               # conexión a MySQL leyendo variables de entorno
├── gunicorn.conf.py    # configuración del servidor para Render
├── requirements.txt    # dependencias (incluye gunicorn)
├── .python-version     # versión de Python para Render (3.12)
├── .env.example        # plantilla de variables (copiar a .env)
├── .gitignore          # evita subir .env, ca.pem y venv
├── sql/tareas_db.sql   # script de creación de la BD (XAMPP)
├── templates/          # páginas HTML
└── static/estilos.css
```

## Ejecutar en local (XAMPP)

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # y editar datos
python app.py
```

Abrir http://127.0.0.1:5000 y http://127.0.0.1:5000/salud

## Render

| Campo | Valor |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn -c gunicorn.conf.py app:app` |
| Secret File | `ca.pem` (certificado de Aiven) |
| DB_SSL_CA | `/etc/secrets/ca.pem` |

Variables: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_SSL_CA`, `SECRET_KEY`.


## Bitácora - Parte B Aiven

- **Service:** mysql-2d1594de.
- **Host:** mysql-2d1594de-gonzalezferjud-c0b6.c.aivencloud.com
- **Port:** 15321
- **User:** avnadmin
- **Database:** defaultdb
- **Estado:** Running
- **CA:** ca.pem descargado# tareas-cecytem-equipo5
