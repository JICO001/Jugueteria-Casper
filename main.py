# Bloque de importación de biliotecas: 
# func.inv: Biblioteca de funciones Python 
# sql_func: Biblioteca de funciones SQL 

import func_inv as fn
import sql_func as sql

# Al inicio del programa, se crea o se verifica que exista la db Inventario y crea una tabla dentro "inventarioJugeteria". 

sql.crear_tabla()

# Funciones que Unifican las opciones de los sub-Menues "Registrar Producto", "Consultar Productos" y "Gestionar Productos"
# Sirve para: 
# 1) Mantener abierto el sub-menu mientras se trabaja dentro. 
# 2) Validaciones de carga de datos.
# 3) Manejo de errores. 
# 4) Recolección de datos de carga para posterior visualización.

def registrar_nuevo_producto(ultimos_registros,categorias):

    """
    Gestiona el proceso de registro de nuevos productos en el inventario.

    Parámetros:
        ultimos_registros (list): Lista que almacena los productos
            registrados durante la sesión actual del programa.
        categorias (list): Lista de categorías disponibles para
            clasificar los productos.

    Solicita y valida los datos del producto mediante las funciones
    de func_inv. Muestra un resumen para confirmar el registro y,
    si el usuario confirma, utiliza sql.registrar_producto() para
    guardarlo en la base de datos.

    Si el registro se realiza correctamente, consulta el producto
    registrado, lo muestra en pantalla y lo agrega a ultimos_registros.

    Permite registrar varios productos consecutivamente. Finaliza
    el proceso si el usuario decide volver al menú principal o si
    se agotan los intentos de alguna validación.

    No retorna ningún valor explícito.
    """

    carga = "si"

    while carga == "si":

        nombre = fn.input_nombre()
        if nombre is True:
            break

        descripcion = fn.input_descripcion()

        cantidad = fn.input_cantidad()
        if cantidad == 0:
            break

        precio = fn.input_precio()
        if precio == 0:
            break

        categoria = fn.opciones_categorias(categorias)
        if categoria is True:
            break

        
        fn.mensaje_aviso(
            f"\nVerifique que los datos sean correctos.\n\n"
            f"Nombre: {nombre}.\n"
            f"Descripción: {descripcion}.\n"
            f"Cantidad: {cantidad}\n"
            f"Precio: {precio}\n"
            f"Categoría: {categoria}\n"
            f"\nPara registrar el producto, escriba si.\n"
            f"Para descartar el producto escriba no."
        )

        confirmacion = fn.boton_si_no()
        match confirmacion:
            case True:
                break
            case "no":
                fn.mensaje_aviso("\nPara ingresar otro producto, escriba si. \nPara volver al menú principal escriba no")
                bucle = fn.boton_si_no()
                if bucle is True:
                    break 
                elif bucle == "no":
                    break
                else:
                    continue
            case "si":
                fn.mensaje_ok(f"\nDatos cargados correctamente.\n")
            case _:
                fn.mensaje_error("Error! Volviendo al menú principal...")
                break
                
        id_ultimo_registro = sql.registrar_producto(nombre,descripcion,cantidad,precio,categoria)

        if id_ultimo_registro is not None:
            ultimo_registro = sql.buscar_producto(id_ultimo_registro)
            fn.print_tabla_unico(ultimo_registro)

            ultimos_registros.append(ultimo_registro)

        fn.mensaje_aviso("\nPara ingresar otro producto, escriba si. \nPara volver al menú principal escriba no")

        carga = fn.boton_si_no()
        if carga is True:
            break 

def consultar_productos(categorias,ultimos_registros):

    """
    Gestiona el submenú de consultas del inventario.

    Parámetros:
        categorias (list): Lista de categorías disponibles para
            filtrar los productos.
        ultimos_registros (list): Lista de productos registrados
            durante la sesión actual del programa.

    Muestra el menú de consultas y ejecuta la función correspondiente
    de func_inv según la opción seleccionada.

    Permite realizar varias consultas consecutivas sin salir
    del submenú.

    Finaliza el ciclo si el usuario selecciona volver al menú principal
    o si se agotan los intentos de selección del menú.

    No retorna ningún valor explícito.
    """

    while True:
        menu_2 = fn.menu_consultar_productos()

        if menu_2 is True:
            break

        match menu_2:
            case 1:
                fn.buscar_producto_id()
            case 2:
                fn.visualizar_todos_los_productos()
            case 3:
                fn.productos_segun_stock()
            case 4:
                fn.buscar_productos_por_nombres()
            case 5:
                fn.filtrar_productos_por_categoria(categorias)
            case 6:
                fn.ver_ultimos_productos_registrados(ultimos_registros)
            case 7:
                break
            case _:
                fn.mensaje_error("Error, volviendo al menú principal...")
                break

def gestionar_productos(categorias):

    """
    Gestiona el submenú de modificación y eliminación de productos
    del inventario.

    Parámetros:
        categorias (list): Lista de categorías disponibles para
            asignar a los productos.

    Muestra el menú de gestión y ejecuta la función correspondiente
    de func_inv según la opción seleccionada.

    Permite actualizar el nombre, la descripción, la cantidad,
    el precio o la categoría de un producto, así como eliminarlo.

    Permite realizar varias operaciones consecutivas sin salir
    del submenú.

    Finaliza el ciclo si el usuario selecciona volver al menú principal
    o si alguna función de gestión devuelve True.

    No retorna ningún valor explícito.
    """

    while True:
        menu_3 = fn.menu_gestionar_productos()

        if menu_3 is True:
            break
    
        match menu_3:
            case 1:
                uno = fn.actualizar_nombre_de_un_producto()
                if uno is True:
                    break
                elif uno == "no":
                    continue
                else:
                    continue

            case 2:
                dos = fn.actualizar_descripcion_de_un_producto()
                if dos is True:
                    break
                elif dos == "no":
                    continue
                else:
                    continue
            case 3:
                tres = fn.actualizar_cantidad_de_un_producto()
                if tres is True:
                    break
                elif tres == "no":
                    continue
                else:
                    continue

            case 4:
                cuatro = fn.actualizar_precio_de_un_producto()
                if cuatro is True:
                    break
                elif cuatro == "no":
                    continue
                else:
                    continue

            case 5:
                cinco = fn.actualizar_categoria_de_un_producto(categorias)
                if cinco is True:
                    break
                elif cinco == "no":
                    continue
                else:
                    continue

            case 6:
                seis = fn.eliminar_un_producto()
                if seis is True:
                    break
                elif seis == "no":
                    continue
                else:
                    continue

            case 7:
                break
            case _:
                continue


# Listas Locales que almacenan datos especificos del inventario:
# Sirven para: 
# 1) Almacenar datos de la sesión (ultimos_registros)
# 2) Datos de consulta para las opciones de categorías actuales (es una lista local, para el fácil acceso de actualización)

ultimos_registros = []
categorias = [
    "Primera infancia",
    "Muñecas y bebotes",
    "Muñecos y figuras de acción",
    "Peluches",
    "Vehículos y pistas",
    "Bloques y construcción",
    "Juegos de mesa y cartas",
    "Rompecabezas",
    "Juguetes didácticos y educativos",
    "Arte y manualidades",
    "Juguetes musicales",
    "Deportes y aire libre",
    "Juegos de roles y profesiones",
    "Disfraces y accesorios",
    "Juguetes electrónicos",
    "Juguetes antiestrés y de colección"
]



# Ejecución del programa: 
# Muestra el menú principal.
# Unifica las tres funciones locales y las separa en las opciones elegibles del menú principal.
# Mantiene el programa corriendo hasta que el usuario lo cierre.
# El programa se mantiene abierto a pesar de errores predecibles. 

while True: 
     boton = fn.menu_principal()
     

     match boton:

      case 1:
            registrar_nuevo_producto(ultimos_registros,categorias)

      case 2:
            consultar_productos(categorias,ultimos_registros)

      case 3:

            gestionar_productos(categorias)
                              
      case 4: 
            fn.mensaje_aviso("\nSaliendo del programa...\n")
            raise SystemExit

      case _:
            continue

