import sql_func as sql
from typing import Literal


def menu_principal():

    """
    Muestra en pantalla las opciones disponibles del menú principal
    y solicita al usuario que seleccione una.

    Utiliza boton_opciones() para validar la selección.

    Retorna:
        int: Número de la opción seleccionada.
        None: Si el ingreso es inválido.
    """
    menu_principal = [
        "Registrar nuevos productos",
        "Consultar productos",
        "Gestionar productos",
        "Salir"
    ]
    print("-" * 119)
    for i, opcion in enumerate(menu_principal, start=1):
        print(f"{i}. {opcion}")

    boton = boton_opciones(menu_principal)
    return boton


def boton_opciones(opciones):

    """
    Solicita al usuario un número y valida que se encuentre dentro
    del rango de opciones disponibles.

    Parámetros:
        opciones (list): Lista de opciones que determina el rango
                        de números permitidos.

    Retorna:
        int: Número ingresado por el usuario si es válido.
        None: Si el usuario ingresa un valor no numérico o fuera
            del rango permitido.
    """
    try:
        boton = int(input("\nEscribe el número de la opción que quieres elegir: "))

        if not 1 <= boton <= len(opciones):
            print(f"\nError: escribe un número del 1 al {len(opciones)}")
            return None

    except ValueError:
        print(f"\nError: debes ingresar un número del 1 al {len(opciones)}")
        return None

    except Exception as error:
        print(f"\nError inesperado: {error}")
        return None

    return boton

def input_nombre():

    """
    Solicita el nombre del producto y valida que el campo no esté vacío.

    Permite hasta cinco intentos de ingreso. Convierte el texto a
    mayúsculas y elimina los espacios al inicio y al final.

    Retorna:
        str: Nombre del producto validado.
        True: Si se agotan los cinco intentos sin ingresar un nombre válido.
    """

    for intentos in range(5):
        nombre = input("\nIngrese el nombre del producto: ").upper().strip()

        if not nombre or nombre == " ":
            print("\nEl campo no puede quedar vacío")
            if intentos == 4:
                print("\nDemasiados intentos, volviendo al menú principal...")
                return True
            continue 

        return nombre

def input_descripcion():

    """
    Solicita la descripción del producto.

    El ingreso es opcional. Convierte el texto a mayúsculas y elimina
    los espacios al inicio y al final.

    Retorna:
        str: Descripción ingresada por el usuario. Puede ser una cadena
            vacía si no se proporciona una descripción.
    """
    descripcion = input("\nIngrese una descripción del producto (opcional): ").upper().strip()
    return descripcion

def input_cantidad():

    """
    Solicita la cantidad de unidades del producto y valida que sea
    un número entero positivo.

    Permite hasta cinco intentos de ingreso.

    Retorna:
        int: Cantidad ingresada si es un número entero mayor que cero.
        0: Si se agotan los cinco intentos o ocurre un error inesperado.
    """
    
    for intentos in range(5):
        try:
            cantidad = int(input("\nIngrese la cantidad del producto: "))

        except ValueError:
            print("\nError: El valor tiene que ser un número entero positivo")

        except Exception as error:
            print(f"Error inesperado {error}\n Volviendo al menú principal...")
            return 0

        else: 
            if cantidad > 0:
                return cantidad
            
            print("\nError: El valor tiene que ser un número entero positivo")
     
        if intentos == 4:
            print("\nDemasiados intentos, volviendo al menú principal...")
            return 0    

def input_precio():

    """
    Solicita el precio del producto y valida que sea un número real
    positivo.

    Permite hasta cinco intentos de ingreso.

    Retorna:
        float: Precio ingresado si es un número mayor que cero.
        0: Si se agotan los cinco intentos o ocurre un error inesperado.
    """
    
    for intentos in range(5):
        try:
            precio = float(input("\nIngrese el precio del producto: "))

        except ValueError:
            print("\nError: El precio tiene que ser un número real positivo")

        except Exception as error:
            print(f"Error inesperado {error}\n Volviendo al menú principal...")
            return 0

        else: 
            if precio > 0:
                return precio
            
            print("\nError: El precio tiene que ser un número real positivo")
     
        if intentos == 4:
            print("\nDemasiados intentos, volviendo al menú principal...")
            return 0    

def elegir_sub_menues(opciones):

    """
    Muestra las opciones de un submenú y solicita al usuario que
    seleccione una mediante su número.

    Parámetros:
        opciones (list): Lista de opciones disponibles.

    Permite hasta cinco intentos de selección. Utiliza
    boton_opciones() para validar el número ingresado.

    Retorna:
        int: Número de la opción seleccionada.
        True: Si se agotan los cinco intentos.
    """

    
    for i, opcion in enumerate(opciones, start=1):
            print(f"{i}. {opcion}")
    
    for intentos in range(5):
        boton = boton_opciones(opciones)

        if boton is not None:
            return boton

        if intentos == 4:
            print("\nDemasiados intentos, volviendo al menú principal...")
            return True
        
        print("\nIngresa una opción válida.")


        

def opciones_categorias(opciones):
    """
    Muestra las categorías disponibles y permite seleccionar una.

    Parámetros:
        opciones (list): Lista de categorías disponibles.

    Permite hasta cinco intentos de selección. Si el usuario ingresa
    una opción inválida, solicita nuevamente la selección.

    Retorna:
    str: Categoría seleccionada, convertida a mayúsculas y sin
        espacios al inicio o al final.
    True: Si se agotan los cinco intentos de selección.
    """

    print("\nCATEGORÍAS DE PRODUCTOS\n")

    for i, opcion in enumerate(opciones, start=1):
                print(f"{i}. {opcion}")
        
    for intentos in range(5):
        boton = boton_opciones(opciones)

        if boton is not None:
            return opciones[boton - 1].upper().strip()

        print("\nIngresa una opción válida.")

        if intentos == 4:
            print("\nDemasiados intentos, volviendo al menú principal...")
            return True

def boton_si_no() -> Literal["si", "no", True]:
    """
    Solicita al usuario una respuesta de confirmación y valida que
    sea estrictamente "si" o "no".

    Permite hasta cinco intentos de ingreso.

    Retorna:
        str: "si" o "no" si la respuesta es válida.
        True: Si se agotan los cinco intentos de ingreso.
    """
    
    for intentos in range(5):

        si = (input("\n(si/no): ")).strip().lower()
     
        if not si or si == " " or (si != "si" and si != "no"):
         print("Error! Escriba si o no")
         if intentos == 4:
            print("\nDemasiados intentos, volviendo al menú principal...\n\n") 
            return True

         continue
            
        return si 




def menu_consultar_productos():
    """
    Muestra las opciones disponibles para consultar los productos
    registrados en el inventario.

    Utiliza elegir_sub_menues() para mostrar las opciones y validar
    la selección.

    Retorna:
        int: Número de la opción seleccionada.
        True: Si se agotan los cinco intentos de selección.
    """
    menu_consultas = [
        "Buscar producto por ID",
        "Visualizar todos los productos",
        "Consultar productos según stock",
        "Buscar productos por nombre",
        "Filtrar productos por categoría",
        "Ver productos registrados en esta sesión",
        "Volver al menú principal"
    ]
    print("-" * 119)
    elegir = elegir_sub_menues(menu_consultas)
    return elegir

def encabezado_tabla():

    """
    Muestra en pantalla los encabezados de las columnas de la tabla
    de productos y una línea separadora.

    No recibe parámetros ni retorna valores.
    """
    
    print(
        f"\n{'ID':<5}"
        f"{'NOMBRE':<25}"
        f"{'DESCRIPCIÓN':<30}"
        f"{'CANTIDAD':<12}"
        f"{'PRECIO':<12}"
        f"{'CATEGORÍA':<35}"
    )

    print("-" * 119)

def contenido_tabla(producto):
    """
    Muestra en pantalla los datos de un producto en formato de tabla.
    Limita la longitud de los textos para mantener alineadas las columnas.
    """

    descripcion = producto[2] or ""
    nombre = producto[1]

    if len(nombre) > 22:
        nombre = nombre[:18] + "..."

    if len(descripcion) > 27:
        descripcion = descripcion[:24] + "..."


    print(
        f"{producto[0]:<5}"
        f"{nombre:<25}"
        f"{descripcion:<30}"
        f"{producto[3]:<12}"
        f"${producto[4]:<11.2f}"
        f"{producto[5]:<35}"
    )

def print_tabla_varios(tabla_productos):
    """
    Muestra en pantalla una lista de productos en formato de tabla.

    Parámetros:
        tabla_productos (list[tuple]): Lista de tuplas con los datos de los productos a visualizar.

    Si la lista contiene productos, muestra el encabezado y los datos
    de cada registro. Si está vacía o es None, informa que no hay
    productos para mostrar.

    No retorna ningún valor.
    """
    if tabla_productos:
        encabezado_tabla()
    
        for producto in tabla_productos:
            contenido_tabla(producto)
    
    else:
        print("\nNo hay productos para mostrar.\n")

def print_tabla_unico(producto):
    """
    Muestra en pantalla los datos de un único producto en formato de tabla.

    Parámetros:
        producto (tuple): Tupla con los datos del producto encontrado.
        None: Si no se encontró un producto para mostrar.

    Si el producto existe, muestra el encabezado y sus datos.
    De lo contrario, informa que no fue encontrado.

    No retorna ningún valor.
    """
    if producto is not None:
         encabezado_tabla()
         contenido_tabla(producto)
    else:
        print("Producto no encontrado.")

def validacion_id():
    """
    Solicita el ID de un producto y valida que sea un número entero
    positivo.

    Permite hasta cinco intentos de ingreso.

    Retorna:
        int: ID ingresado si es un número entero mayor que cero.
        True: Si se agotan los cinco intentos o ocurre un error inesperado.
    """
    for intentos in range(5):
        try:
            id_busqueda = int(input("\nIngrese el id del producto: "))

        except ValueError:
            print("\nError: El valor tiene que ser un número entero positivo")

        except Exception as error:
            print(f"Error inesperado {error}\n Volviendo al menú principal...")
            return True

        else: 
            if id_busqueda > 0:
                return id_busqueda
            
            print("\nError: El valor tiene que ser un número entero positivo")
     
        if intentos == 4:
            print("\nDemasiados intentos, volviendo al menú principal...")
            return True




def buscar_producto_id():
    """
    Solicita el ID de un producto, consulta si existe en el inventario
    y muestra sus datos en pantalla.

    Utiliza validacion_id() para validar el ID y
    sql.buscar_producto() para realizar la consulta en la base de datos.

    Retorna:
        int: ID del producto encontrado.
        True: Si el ID no es válido, no se encuentra el producto
            o se agotan los intentos de ingreso.
    """
    id_busqueda = validacion_id()

    if id_busqueda is True:
        return True
        
    encontrado = sql.buscar_producto(id_busqueda)
    if encontrado is not None:
        print_tabla_unico(encontrado)
        return id_busqueda 
    else:
        print("No se encontro el producto")
        return True 
   
def visualizar_todos_los_productos():
    """
    Obtiene todos los productos registrados en el inventario y los
    muestra en pantalla mediante una tabla.

    No recibe parámetros ni retorna valores.
    """
    lista_completa = sql.obtener_productos()
    print_tabla_varios(lista_completa)

def productos_segun_stock():
    """
    Solicita una cantidad límite y muestra los productos cuya cantidad
    disponible es igual o inferior a ese valor.

    Utiliza input_cantidad() para validar el límite y
    sql.reporte_productos_segun_limite() para consultar los registros.

    Si la validación falla, finaliza la función sin realizar la consulta.

    No retorna ningún valor.
    """
    limite = input_cantidad()

    if limite == 0:
        return

    reporte_productos = sql.reporte_productos_segun_limite(limite)
    print_tabla_varios(reporte_productos)

def buscar_productos_por_nombres():
    """
    Solicita el nombre o una parte del nombre de un producto y muestra
    los registros que contienen ese texto.

    Utiliza input_nombre() para validar el ingreso y
    sql.obtener_productos_por_coincidencia_nombre() para realizar
    la consulta en la base de datos.

    Si se agotan los intentos de ingreso, finaliza la función.

    No retorna ningún valor.
    """
    nombre_producto = input_nombre()

    if nombre_producto is True:
        return

    coincidencias = sql.obtener_productos_por_coincidencia_nombre(nombre_producto)
    print_tabla_varios(coincidencias)

def filtrar_productos_por_categoria(categorias):
    """
    Muestra las categorías disponibles, permite seleccionar una
    y muestra los productos que pertenecen a esa categoría.

    Parámetros:
        categorias (list): Lista de categorías disponibles.

    Utiliza opciones_categorias() para validar la selección y
    sql.obtener_productos_por_categoria() para consultar los registros.

    Si se agotan los intentos de selección, finaliza la función.

    No retorna ningún valor.
    """
    categoria = opciones_categorias(categorias)

    if categoria is True:
        return
    
    productos_filtrados = sql.obtener_productos_por_categoria(categoria)
    print_tabla_varios(productos_filtrados)

def ver_ultimos_productos_registrados(ultimos_registros):
    """
    Muestra en pantalla los productos registrados durante la sesión
    actual del programa.

    Parámetros:
        ultimos_registros (list[tuple]): Lista de tuplas que contiene
        los productos registrados durante la sesión actual.

    No retorna ningún valor.
    """
    print_tabla_varios(ultimos_registros)





def menu_gestionar_productos():
    """
    Muestra en pantalla las opciones disponibles para gestionar
    los productos registrados en el inventario.

    No recibe parámetros ni retorna valores.
    """
    menu_gestionar = [
        "Actualizar nombre de un producto",
        "Actualizar descripción de un producto",
        "Actualizar cantidad de un producto",
        "Actualizar precio de un producto",
        "Actualizar categoría de un producto",
        "Eliminar un producto",
        "Volver al menú principal"
    ]
    print("-" * 119)
    elegir = elegir_sub_menues(menu_gestionar)
    return elegir

def actualizar_nombre_de_un_producto():
    """
    Solicita el ID de un producto, muestra sus datos y permite
    ingresar un nuevo nombre.

    Utiliza buscar_producto_id() para identificar el producto,
    input_nombre() para validar el nuevo nombre y
    sql.actualizar_nombre() para modificar el registro.

    Si el producto no se encuentra o falla la validación del nombre,
    finaliza la función.

    Retorna:
        True: Si se agotan los intentos de confirmación o de ingreso
            del nuevo nombre.
        "no": Si el usuario cancela la modificación.
        None: Si se realiza la modificación o la función finaliza
            sin efectuarla.
    """
    id = buscar_producto_id()
    if id is True:
        return

    print("Quieres modificar este producto? (si/no)")
    confirmacion = boton_si_no()
    match confirmacion:
        case True:
            return True
        case "no":
            return "no"
        case "si":
            nombre_nuevo = input_nombre()
            if nombre_nuevo is True:
                return True
            sql.actualizar_nombre(id,nombre_nuevo)

def actualizar_descripcion_de_un_producto():
    """
    Solicita el ID de un producto, muestra sus datos y permite
    ingresar una nueva descripción.

    Utiliza buscar_producto_id() para identificar el producto,
    input_descripcion() para obtener la nueva descripción y
    sql.actualizar_descripcion() para modificar el registro.

    Si el producto no se encuentra, finaliza la función.

    Retorna:
        True: Si se agotan los intentos de confirmación.
        "no": Si el usuario cancela la modificación.
        None: Si se realiza la modificación o la función finaliza
            sin efectuarla.
    """
    id = buscar_producto_id()
    if id is True:
        return

    print("Quieres modificar este producto? (si/no)")
    confirmacion = boton_si_no()

    match confirmacion:
        case True:
            return True
        case "no":
            return "no"
        case "si":
            descripcion_nueva = input_descripcion()
            sql.actualizar_descripcion(id,descripcion_nueva)

def actualizar_cantidad_de_un_producto():
    """
    Solicita el ID de un producto, muestra sus datos y permite
    ingresar una nueva cantidad de unidades.

    Utiliza buscar_producto_id() para identificar el producto,
    input_cantidad() para validar la nueva cantidad y
    sql.actualizar_cantidad() para modificar el registro.

    Si el producto no se encuentra o falla la validación,
    finaliza la función.

    Retorna:
        True: Si se agotan los intentos de confirmación.
        "no": Si el usuario cancela la modificación.
        None: Si se realiza la modificación o la función finaliza
            sin efectuarla.
    """
    id = buscar_producto_id()
    if id is True:
        return 
    print("Quieres modificar este producto? (si/no)")
    confirmacion = boton_si_no()
    match confirmacion:
        case True:
            return True
        case "no":
            return "no"
        case "si":
            cantidad_nueva = input_cantidad()
            if cantidad_nueva == 0:
                return
            sql.actualizar_cantidad(id,cantidad_nueva)

def actualizar_precio_de_un_producto():
    """
    Solicita el ID de un producto, muestra sus datos y permite
    ingresar un nuevo precio.

    Utiliza buscar_producto_id() para identificar el producto,
    input_precio() para validar el nuevo precio y
    sql.actualizar_precio() para modificar el registro.

    Si el producto no se encuentra o falla la validación,
    finaliza la función.

    Retorna:
        True: Si se agotan los intentos de confirmación.
        "no": Si el usuario cancela la modificación.
        None: Si se realiza la modificación o la función finaliza
            sin efectuarla.
    """
    id = buscar_producto_id()
    if id is True:
        return 
    print("Quieres modificar este producto? (si/no)")
    confirmacion = boton_si_no()
    match confirmacion:
        case True:
            return True
        case "no":
            return "no"
        case "si":
            precio_nuevo = input_precio()
            if precio_nuevo == 0:
                return
            sql.actualizar_precio(id,precio_nuevo)

def actualizar_categoria_de_un_producto(categorias):
    """
    Solicita el ID de un producto, muestra sus datos y permite
    seleccionar una nueva categoría.

    Parámetros:
        categorias (list): Lista de categorías disponibles.

    Utiliza buscar_producto_id() para identificar el producto,
    opciones_categorias() para validar la nueva categoría y
    sql.actualizar_categoria() para modificar el registro.

    Si el producto no se encuentra o falla la selección de categoría,
    finaliza la función.

    Retorna:
        True: Si se agotan los intentos de confirmación.
        "no": Si el usuario cancela la modificación.
        None: Si se realiza la modificación o la función finaliza
            sin efectuarla.
    """
    id = buscar_producto_id()
    if id is True:
        return
    print("Quieres modificar este producto? (si/no)")
    confirmacion = boton_si_no()
    match confirmacion:
        case True:
            return True
        case "no":
            return "no"
        case "si":
            categoria_nueva = opciones_categorias(categorias)
            if categoria_nueva == True:
                return
            sql.actualizar_categoria(id,categoria_nueva)

def eliminar_un_producto():
    """
    Solicita el ID de un producto, muestra sus datos y pide
    confirmación antes de eliminar el registro.

    Utiliza buscar_producto_id() para identificar el producto,
    boton_si_no() para obtener la confirmación y
    sql.eliminar_producto() para eliminarlo de la base de datos.

    El producto se elimina únicamente si el usuario responde "si".

    Si el producto no se encuentra, el usuario responde "no"
    o se agotan los intentos de confirmación, no realiza la eliminación.

    No retorna ningún valor explícito.
    """
    id = buscar_producto_id()
    if id is True:
        return
    print("\nQuiere eliminar el producto?\n")
    confirmacion = boton_si_no()
    match confirmacion:
        case "no":
                return
        case True:
                return
        case "si":
                sql.eliminar_producto(id)

    
