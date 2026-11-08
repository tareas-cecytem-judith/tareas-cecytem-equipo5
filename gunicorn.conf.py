# Configuración de Gunicorn para Render
import os

bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"  # Render indica el puerto en PORT
workers = 2
timeout = 60
accesslog = "-"   # registros de acceso visibles en los Logs de Render
errorlog = "-"
loglevel = "info"
