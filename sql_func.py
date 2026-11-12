
import sqlite3
import os
import sys
import shutil
from pathlib import Path


def obtener_directorio_datos():
    """
    Devuelve el directorio permanente de datos del usuario
    según su sistema operativo.
    """

    if sys.platform == "win32":
        directorio = Path(
            os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")
        )

    elif sys.platform == "darwin":
        directorio = Path.home() / "Library" / "Application Support"

    else:
        directorio = Path(
            os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")
        )

    return directorio / "JugueteriaCasper"

def buscar_base_inicial():
    """
    Busca la base de datos de demostración incluida con el programa.
    """

    carpeta_programa = Path(__file__).resolve().parent

    if getattr(sys, "frozen", False):
        carpeta_recursos = Path(sys._MEIPASS)
    else:
        carpeta_recursos = carpeta_programa

    posibles_rutas = [
        carpeta_recursos / "datos_iniciales" / "Inventario.db",
        carpeta_recursos / "Inventario.db",
        carpeta_programa / "datos_iniciales" / "Inventario.db",
        carpeta_programa / "Inventario.db"
    ]

    for ruta in posibles_rutas:
        if ruta.is_file():
            return ruta

    raise FileNotFoundError(
        "No se encontró Inventario.db. "
        "Verifique que la base de datos de demostración "
        "esté incluida con el programa."
    )

def obtener_ruta_base_datos():
    """
    Obtiene la ruta permanente de Inventario.db.

    Si todavía no existe una base local, copia la base
    de demostración sin eliminar el archivo original.
    """

    directorio_datos = obtener_directorio_datos()
    directorio_datos.mkdir(parents=True, exist_ok=True)

    ruta_local = directorio_datos / "Inventario.db"

    if not ruta_local.exists():
        ruta_original = buscar_base_inicial()

        ruta_temporal = ruta_local.with_name("Inventario.db.tmp")

        try:
            shutil.copy2(ruta_original, ruta_temporal)
            ruta_temporal.replace(ruta_local)

        finally:
            if ruta_temporal.exists():
                ruta_temporal.unlink()

    return ruta_local


def conectar():
    """
    Establece una conexión con la base de datos local del usuario.
    """

    ruta_db = obtener_ruta_base_datos()
    conexion = sqlite3.connect(ruta_db)

    return conexion

def crear_tabla():

    """
    Crea la tabla InventarioJugueteria si todavía no existe.

    Estructura de la tabla:
        id: Identificador único autoincremental (INTEGER).
        nombre: Nombre del producto (TEXT, obligatorio).
        descripcion: Descripción del producto (TEXT, opcional).
        cantidad: Cantidad disponible (INTEGER, obligatorio).
        precio: Precio del producto (REAL, obligatorio).
        categoria: Categoría del producto (TEXT, obligatorio).

    No retorna ningún valor.
    
    """

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS InventarioJugueteria (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nombre TEXT NOT NULL,
        descripcion TEXT,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL,
        categoria TEXT NOT NULL
    )
    """)
    conexion.commit()
    conexion.close()



def registrar_producto(nombre,descripcion,cantidad,precio,categoria):

    """
    Registra un producto nuevo en la tabla InventarioJugueteria.

    Parámetros:
        nombre (str): Nombre del producto.
        descripcion (str): Descripción del producto.
        cantidad (int): Cantidad de unidades disponibles.
        precio (float): Precio del producto.
        categoria (str): Categoría a la que pertenece el producto.

    Retorna:
        int: ID asignado al producto si el registro es exitoso.
        None: Si ocurre un error durante el registro.
    
    """

    conexion = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO InventarioJugueteria 
            (nombre,descripcion,cantidad,precio,categoria)
            VALUES (?,?,?,?,?)
        """,(nombre,descripcion,cantidad,precio,categoria))

        id_producto = cursor.lastrowid

        conexion.commit()

        return id_producto

    except sqlite3.Error as error: 
        print(f"\nError al ingresar producto: '{error}'\n")
        return None

    finally:
        if conexion is not None: 
            conexion.close()




def buscar_producto(id_producto):
    """
    Busca un producto en la tabla InventarioJugueteria mediante su ID.

    Parámetros:
        id_producto (int): Identificador del producto a consultar.

    Retorna:
        tuple: Datos del producto encontrado.
        None: Si no existe un producto con ese ID o si ocurre un error.
    """

    conexion = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT * FROM InventarioJugueteria
            WHERE id = ?
        """, (id_producto,))

        producto = cursor.fetchone()

        return producto

    except sqlite3.Error as error:
        print(f"\nError al consultar el producto: {error}\n")
        return None

    finally:
        if conexion is not None:
            conexion.close()

def obtener_productos():

    """
    Obtiene todos los productos registrados en la tabla InventarioJugueteria.

    Parámetros:
        No recibe parámetros.

    Retorna:
        list[tuple]: Lista de tuplas con los datos de todos los productos,
                     ordenados de forma ascendente según su ID.
        None: Si ocurre un error durante la consulta.

    Cada tupla contiene:
        id (int): .
        nombre (str): .
        descripcion (str): .
        cantidad (int): .
        precio (float): .
        categoria (str): .

    """
    conexion = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()


        cursor.execute("""
        
            SELECT *
            FROM InventarioJugueteria
            ORDER BY id
        """)

        productos = cursor.fetchall()
        return productos
    except sqlite3.Error as error:
            print(f"\nError al consultar los productos: {error}\n")
            return None
    
    finally:
        if conexion is not None:
            conexion.close()

def reporte_productos_segun_limite(limite):
    """
    Obtiene los productos cuya cantidad disponible es igual
    o inferior al límite especificado.

    Parámetros:
            limite (int): Cantidad máxima de unidades disponibles
                      para incluir un producto en el reporte.

    Retorna:  
            list[tuple]: Lista de productos que cumplen la condición,
                     ordenados de menor a mayor cantidad.
        None: Si ocurre un error durante la consulta.
    """

    conexion = None

    try:

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT *
        FROM  InventarioJugueteria
        WHERE cantidad <= ?
        ORDER BY cantidad ASC 
        """,(limite,))

        productos = cursor.fetchall()

        return productos


    except sqlite3.Error as error:
            print(f"\nError al generar reporte: {error}\n")
            return None
    
    finally:
        if conexion is not None:
            conexion.close()

def obtener_productos_por_coincidencia_nombre(nombre_productos):
    """
    Obtiene los productos registrados en la tabla InventarioJugueteria
    cuyos nombres contienen el texto buscado.

    Parámetros:
            nombre_productos (str): Texto que se utilizará para buscar
                                    coincidencias parciales en los nombres.

    Retorna:
            list[tuple]: Lista de tuplas con los productos encontrados,
                        ordenados de forma ascendente según su ID.
            []: Si no se encuentran coincidencias.
            None: Si ocurre un error durante la consulta.

    Cada tupla contiene:
            id (int): Identificador único del producto.
            nombre (str): Nombre del producto.
            descripcion (str): Descripción del producto.
            cantidad (int): Cantidad disponible.
            precio (float): Precio del producto.
            categoria (str): Categoría del producto.

    """

    conexion = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT *
            FROM InventarioJugueteria
            WHERE nombre LIKE ?
            ORDER BY id
        """, (f"%{nombre_productos}%",))

        productos = cursor.fetchall()
        return productos

    except sqlite3.Error as error:
        print(f"\nError al consultar los productos: {error}\n")
        return None

    finally:
        if conexion is not None:
            conexion.close()

def obtener_productos_por_categoria(categoria_productos):
    """
    Obtiene los productos registrados en la tabla InventarioJugueteria
    que pertenecen a una categoría determinada.

    Parámetros:
            categoria_productos (str): Categoría seleccionada por el usuario
                                    mediante el menú de opciones.

    Retorna:
            list[tuple]: Lista de tuplas con los productos encontrados,
                        ordenados de forma ascendente según su ID.
            []: Si no se encuentran productos de esa categoría.
            None: Si ocurre un error durante la consulta.

    Cada tupla contiene:
            id (int): Identificador único del producto.
            nombre (str): Nombre del producto.
            descripcion (str): Descripción del producto.
            cantidad (int): Cantidad disponible.
            precio (float): Precio del producto.
            categoria (str): Categoría del producto.
    """

    conexion = None

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT *
            FROM InventarioJugueteria
            WHERE categoria = ?
            ORDER BY id
        """, (categoria_productos,))

        productos = cursor.fetchall()
        return productos

    except sqlite3.Error as error:
        print(f"\nError al consultar los productos: {error}\n")
        return None

    finally:
        if conexion is not None:
            conexion.close()




def actualizar_nombre(id,nuevo_nombre):

    """
    Actualiza el nombre de un producto registrado en la tabla
    InventarioJugueteria, identificándolo mediante su ID.

    Parámetros:
        id (int): Id del producto a modificar.
        nuevo_nombre (str): Nombre que se asignará al producto.

    Retorna:
        None: No devuelve ningún valor.

    """

    conexion = None

    try:

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE InventarioJugueteria
            SET nombre = ?
            WHERE id = ?
        """,(nuevo_nombre,id))
        conexion.commit()

        if cursor.rowcount > 0:
            print("\nNombre actualizado correctamente.\n")

        else: 
            print("\nEl producto no fue encontrado, verifique el id\n")

    except sqlite3.Error as error:
            print(f"\nError al actualizar el nombre: {error}\n")
    
    finally:
        if conexion is not None:
            conexion.close()

def actualizar_descripcion(id,nueva_descripcion):

    """
    Actualiza la descripcion de un producto registrado en la tabla
    InventarioJugueteria, identificándolo mediante su ID.

    Parámetros:
        id (int): Id del producto a modificar.
        nueva_descripcion (str): Descripción que se asignará al producto.

    Retorna:
        None: No devuelve ningún valor.

    """

    conexion = None

    try:

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE InventarioJugueteria
            SET descripcion = ?
            WHERE id = ?
        """,(nueva_descripcion,id))
        conexion.commit()

        if cursor.rowcount > 0:
            print("\nDescripción actualizada correctamente.\n")

        else: 
            print("\nEl producto no fue encontrado, verifique el id\n")

    except sqlite3.Error as error:
            print(f"\nError al actualizar la descripción: {error}\n")
    
    finally:
        if conexion is not None:
            conexion.close()

def actualizar_cantidad(id,nueva_cantidad):

    """
    Actualiza la cantidad de un producto registrado en la tabla
    InventarioJugueteria, identificándolo mediante su ID.

    Parámetros:
        id (int): Id del producto a modificar.
        nueva_cantidad (int): Cantidad que se asignará al producto.

    Retorna:
        None: No devuelve ningún valor.

    """

    conexion = None

    try:

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE InventarioJugueteria
            SET cantidad = ?
            WHERE id = ?
        """,(nueva_cantidad,id))
        conexion.commit()

        if cursor.rowcount > 0:
            print("\nCantidad actualizada correctamente.\n")

        else: 
            print("\nEl producto no fue encontrado, verifique el id\n")

    except sqlite3.Error as error:
            print(f"\nError al actualizar la cantidad: {error}\n")
    
    finally:
        if conexion is not None:
            conexion.close()

def actualizar_precio(id,nuevo_precio):

    """
    Actualiza el precio de un producto registrado en la tabla
    InventarioJugueteria, identificándolo mediante su ID.

    Parámetros:
        id (int): Id del producto a modificar.
        nuevo_precio (float): Precio que se asignará al producto.

    Retorna:
        None: No devuelve ningún valor.

    """

    conexion = None

    try:

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE InventarioJugueteria
            SET precio = ?
            WHERE id = ?
        """,(nuevo_precio,id))
        conexion.commit()

        if cursor.rowcount > 0:
            print("\nPrecio actualizado correctamente.\n")

        else: 
            print("\nEl producto no fue encontrado, verifique el id\n")

    except sqlite3.Error as error:
            print(f"\nError al actualizar el precio: {error}\n")
    
    finally:
        if conexion is not None:
            conexion.close()

def actualizar_categoria(id,nueva_categoria):

    """
    Actualiza la categoria de un producto registrado en la tabla
    InventarioJugueteria, identificándolo mediante su ID.

    Parámetros:
        id (int): Id del producto a modificar.
        nueva_categoria (str): Categoría que se asignará al producto.

    Retorna:
        None: No devuelve ningún valor.

    """

    conexion = None

    try:

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE InventarioJugueteria
            SET categoria = ?
            WHERE id = ?
        """,(nueva_categoria,id))
        conexion.commit()

        if cursor.rowcount > 0:
            print("\nCategoría actualizada correctamente.\n")

        else: 
            print("\nEl producto no fue encontrado, verifique el id\n")

    except sqlite3.Error as error:
            print(f"\nError al actualizar la categoría: {error}\n")
    
    finally:
        if conexion is not None:
            conexion.close()

def eliminar_producto(id):

    """
    Elimina un producto de la tabla InventarioJugueteria,
    identificándolo mediante su ID.

    Parámetros:
        id (int): Id del producto a eliminar.

    Retorna:
        None: No devuelve ningún valor.
    
        
    Verifica si el producto se liminó correctamente o si hubo un error inesperado. 
    """

    conexion = None

    try:

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        DELETE FROM InventarioJugueteria
        WHERE id = ? 
        """,(id,))

        conexion.commit()

        if cursor.rowcount > 0:
            print("\nEl producto ha sido eliminado correctamente.\n")

        else:
            print("\nEl producto no fue encontrado.\n")

    except sqlite3.Error as error:
            print(f"\nError al eliminar un producto: {error}\n")
    
    finally:
        if conexion is not None:
            conexion.close()



