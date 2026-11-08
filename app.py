"""
app.py · TareasCECyTEM
Aplicación Flask para registrar tareas en una base de datos MySQL.
Rutas:
  /                     lista de tareas + formulario para agregar
  /agregar   (POST)     guarda una tarea nueva (INSERT)
  /completar/<id>(POST) marca o desmarca una tarea (UPDATE)
  /eliminar/<id> (POST) borra una tarea (DELETE)
  /salud                prueba de conexión: muestra a qué servidor está conectada la app
"""
import os

from flask import Flask, flash, redirect, render_template, request, url_for

from db import obtener_conexion

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave-solo-para-desarrollo")

PRIORIDADES = ("Baja", "Media", "Alta")


@app.route("/")
def index():
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            cur.execute(
                """
                SELECT t.id, t.titulo, t.descripcion, t.prioridad, t.fecha_limite,
                       t.completada, t.creada_en, c.nombre AS categoria
                FROM tareas t
                JOIN categorias c ON c.id = t.categoria_id
                ORDER BY t.completada ASC, t.creada_en DESC
                """
            )
            tareas = cur.fetchall()
            cur.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
            categorias = cur.fetchall()
    finally:
        conexion.close()

    pendientes = sum(1 for t in tareas if not t["completada"])
    return render_template(
        "index.html",
        tareas=tareas,
        categorias=categorias,
        prioridades=PRIORIDADES,
        pendientes=pendientes,
    )


@app.route("/agregar", methods=["POST"])
def agregar():
    titulo = request.form.get("titulo", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    categoria_id = request.form.get("categoria_id", "")
    prioridad = request.form.get("prioridad", "Media")
    fecha_limite = request.form.get("fecha_limite") or None

    if not titulo or not categoria_id.isdigit() or prioridad not in PRIORIDADES:
        flash("Escribe un título y elige categoría y prioridad.", "error")
        return redirect(url_for("index"))

    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            # Consulta parametrizada (%s): evita inyección SQL
            cur.execute(
                """
                INSERT INTO tareas (titulo, descripcion, categoria_id, prioridad, fecha_limite)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (titulo, descripcion, int(categoria_id), prioridad, fecha_limite),
            )
            nuevo_id = cur.lastrowid
        conexion.commit()  # sin commit el registro NO se guarda
    finally:
        conexion.close()

    flash(f"Tarea #{nuevo_id} guardada en la base de datos.", "ok")
    return redirect(url_for("index"))


@app.route("/completar/<int:tarea_id>", methods=["POST"])
def completar(tarea_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            cur.execute(
                "UPDATE tareas SET completada = 1 - completada WHERE id = %s",
                (tarea_id,),
            )
        conexion.commit()
    finally:
        conexion.close()
    return redirect(url_for("index"))


@app.route("/eliminar/<int:tarea_id>", methods=["POST"])
def eliminar(tarea_id):
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            cur.execute("DELETE FROM tareas WHERE id = %s", (tarea_id,))
        conexion.commit()
    finally:
        conexion.close()
    flash(f"Tarea #{tarea_id} eliminada.", "ok")
    return redirect(url_for("index"))


@app.route("/registros")
def registros():
    """Verificación: muestra las filas tal como están guardadas en la tabla tareas.
    Cada vez que se abre, se consulta de nuevo la base de datos."""
    buscar = request.args.get("buscar", "").strip()
    conexion = obtener_conexion()
    try:
        with conexion.cursor() as cur:
            cur.execute("SELECT @@hostname AS servidor, NOW() AS consultado_en")
            info = cur.fetchone()
            if buscar:
                cur.execute(
                    "SELECT * FROM tareas WHERE titulo LIKE %s ORDER BY id DESC",
                    (f"%{buscar}%",),
                )
            else:
                cur.execute("SELECT * FROM tareas ORDER BY id DESC")
            filas = cur.fetchall()
    finally:
        conexion.close()
    return render_template("registros.html", filas=filas, info=info, buscar=buscar)


@app.route("/salud")
def salud():
    """Evidencia de conexión: servidor, versión, base de datos y SSL."""
    try:
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cur:
                cur.execute(
                    "SELECT @@hostname AS servidor, VERSION() AS version, DATABASE() AS base"
                )
                info = cur.fetchone()
                cur.execute("SHOW SESSION STATUS LIKE 'Ssl_cipher'")
                fila = cur.fetchone()
                info["ssl"] = fila["Value"] if fila and fila["Value"] else "Sin SSL"
                cur.execute("SELECT COUNT(*) AS total FROM tareas")
                info["total_tareas"] = cur.fetchone()["total"]
        finally:
            conexion.close()
        return render_template("salud.html", ok=True, info=info)
    except Exception as error:  # se muestra el error para poder diagnosticarlo
        return render_template("salud.html", ok=False, error=repr(error)), 500


if __name__ == "__main__":
    # Solo para pruebas locales. En Render la app la arranca Gunicorn.
    app.run(debug=True)
