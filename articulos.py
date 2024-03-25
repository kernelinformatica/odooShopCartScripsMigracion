from xmlrpc import client
from datetime import datetime
# Credenciales conección  db odoo
import conn.odoo
db = conn.odoo.db
user = conn.odoo.user
password = conn.odoo.password
# The common XML.RPC endpoint
srv = "http://10.0.0.222:8069"

common = client.ServerProxy("%s/xmlrpc/2/common" % srv)
uid = common.authenticate(db, user, password, {})
api = client.ServerProxy('%s/xmlrpc/2/object'% srv)
datos = []
def tomarDatosArticulosSybase(op, codigo):
    # deberia implementar algun token de seguridad en estas consultas, despúes se vera cual es la mejor manera.
    # Si "op = 0" traer todos los productos
    # Si "op = 1" busca un artículo por código y código de barra
    # Si "op = 2" busca un articulo por codigo de grupo por la variable codigo"

    print("Conecto con Sybase para traer los articulos :::: "+op+" - "+codigo)
    print("Aguarde un momento por favor ...")
    import conn.sybase
    global datos
    cursor = conn.sybase.conn.cursor()


    if op == "1":
        # Trae artículos por codigo de articulo
        print("Trae artículos por codigo de articulo ---> " + codigo)
        cursor.execute("SELECT fac_articulos.art_iva_ri, fac_articulos.art_iva_rni, fac_articulos.id, fac_articulos.art_codigo, fac_articulos.art_descri, fac_precios.art_barras, fac_articulos.art_prec_compra, fac_precios.pre_precio, fac_precios.pre_gondola, departasub.odoo_codigo as categoria_codigo_odoo,  fac_articulos.art_comentario as observa from fac_articulos, fac_precios, departasub where fac_articulos.art_codigo =  fac_precios.art_codigo and departasub.codigo = fac_articulos.art_grupo and fac_precios.pre_lista = 1 and fac_articulos.art_descri > '' and art_descri <> 'CODIGO LIBRE' and fac_articulos.art_grupo not in(42,46,47,17) and fac_precios.art_barras <> fac_precios.art_codigo  and  fac_articulos.art_codigo = '"+codigo+"' and fac_precios.art_barras > ''")
    elif op == "2":
     # Trae por cadigo de grupo
     print("Trae por codigo de grupo ---> "+codigo)
     cursor.execute("SELECT fac_articulos.art_iva_ri, fac_articulos.art_iva_rni, fac_articulos.id, fac_articulos.art_codigo, fac_articulos.art_descri, fac_precios.art_barras, fac_articulos.art_prec_compra, fac_precios.pre_precio, fac_precios.pre_gondola, departasub.odoo_codigo as categoria_codigo_odoo, fac_articulos.art_comentario as observa  from fac_articulos, fac_precios, departasub  where fac_articulos.art_codigo =  fac_precios.art_codigo  and departasub.codigo = fac_articulos.art_grupo and fac_precios.pre_lista = 1 and fac_articulos.art_descri > '' and art_descri <> 'CODIGO LIBRE' and fac_articulos.art_grupo not in(42,46,47,17) and fac_precios.art_barras <> fac_precios.art_codigo 8 and fac_articulos.art_grupo = "+codigo+" and fac_precios.art_barras > ''")
    elif op == "0":
        # Trae todos los artículos
        print("Trae todos los artículos ---> " + codigo)
        cursor.execute(
            "SELECT   fac_articulos.art_iva_ri, fac_articulos.art_iva_rni, fac_articulos.id, fac_articulos.art_codigo, fac_articulos.art_descri, fac_precios.art_barras, fac_articulos.art_prec_compra, fac_precios.pre_precio, fac_precios.pre_gondola, departasub.odoo_codigo as categoria_codigo_odoo, fac_articulos.art_comentario as observa  from fac_articulos, fac_precios, departasub  where fac_articulos.art_codigo =  fac_precios.art_codigo  and departasub.codigo = fac_articulos.art_grupo and fac_precios.pre_lista = 1 and fac_articulos.art_descri > '' and art_descri <> 'CODIGO LIBRE' and fac_articulos.art_grupo not in(42,46,47,17) and fac_precios.art_barras <> fac_precios.art_codigo  and  fac_precios.art_barras > ''")
    elif op == "-1":
        cursor.execute(
            "SELECT fac_articulos.art_iva_ri, fac_articulos.art_iva_rni, fac_articulos.id, fac_articulos.art_codigo, fac_articulos.art_descri, fac_precios.art_barras, fac_articulos.art_prec_compra, fac_precios.pre_precio, fac_precios.pre_gondola, departasub.odoo_codigo as categoria_codigo_odoo, fac_articulos.art_comentario as observa from fac_articulos, fac_precios, departasub where fac_articulos.art_codigo =  fac_precios.art_codigo and departasub.codigo = fac_articulos.art_grupo and fac_precios.pre_lista = 1 and fac_articulos.art_descri > '' and art_descri <> 'CODIGO LIBRE' and fac_articulos.art_grupo not in(42,46,47,17) and fac_precios.art_barras <> fac_precios.art_codigo    and  fac_articulos.art_codigo = '" + codigo + "' and fac_precios.art_barras > ''")

    articulos = cursor.fetchall()
    if len(articulos) > 0:
        for a in articulos:
            publicado = True
            tipo = "consu"
            # tipo = consu : Consumible; product : Producto; service : Servicio
            abm = op
            id_auto = a.id
            precio = a.pre_precio
            precioCosto = a.art_prec_compra
            descripcion= a.art_descri
            codigoBarra = a.art_barras
            codigoArticulo = a.art_codigo
            categoriaOdoo = a.categoria_codigo_odoo
            ivaRi = a.art_iva_ri
            ivaRni = a.art_iva_rni
            fechaHoraHoy = datetime.now()
            if a.observa == None or a.observa == "":
                 observaciones = "Actualizado / Creado  desde Api el "+str(fechaHoraHoy)
            else:
                observaciones = a.observa

            if categoriaOdoo == 0:
                categoriaOdoo = 1

            datos.append([abm, id_auto, codigoArticulo,descripcion, codigoBarra, precio, categoriaOdoo, precioCosto, ivaRi, ivaRni, publicado,  tipo, observaciones])
            #print(f"{abm}\{codigoArticulo}\t{descripcion}\t{codigoBarra}\t$ {precio}\t {categoriaOdoo}\t {precioCosto}t{ivaRi}\t {ivaRni}\t {publicado}")
    else:
        print("La busqueda no arrojo resultados")


# procesas los datos
def procesarArticulos(datos):
    # En esta función los datos pueden ser alterados.
    # Ejemplo: le agregamos el iva al precio original
    datos_nuevos = []
    #codigoArticulo,descripcion, codigoBarra, precio
    for abm, id_auto, codigoArticulo, descripcion, codigoBarra, precio, categoriaOdoo, precioCosto, ivaRi, ivaRni, publicado,  tipo, observaciones in datos:
        datos_nuevos.append([abm, id_auto, codigoArticulo,descripcion,codigoBarra,float(precio), categoriaOdoo, float(precioCosto), ivaRi, ivaRni, bool(publicado),  tipo, observaciones])
        datos = datos_nuevos
        print(datos)

# actualizar los datos en odoo
def actualizarDatosArticulos(datos):
    for abm, id_auto, codigoArticulo, descripcion, codigoBarra, precio, categoriaOdoo, precioCosto, ivaRi, ivaRni, publicado, tipo, observaciones in datos:
        domain = [('default_code', '=', int(codigoArticulo))]
        id = api.execute_kw(db, str(uid), password, "product.template", "search", [domain])
        if not id:
            print("--> Se agrego el articulo "+descripcion)
            r = api.execute_kw(db, uid, password, "product.template", "create", [{'id': int(id_auto), 'is_published': bool(publicado), 'active' : True,  'detailed_type' : 'consu', 'name': str(descripcion), 'list_price': float(precio), 'default_code': codigoArticulo, 'barcode': codigoBarra, 'categ_id' : int(categoriaOdoo), 'standard_price' : float(precioCosto), 'description': observaciones}])
        else:
            if abm == "-1" :
                print("--> Se borra el registro: "+codigoArticulo+" id auto: "+str(id_auto))
                r = api.execute_kw(db, uid, password, "product.template", "unlink", [id])
            else:
                r = api.execute_kw(db, uid, password, "product.template", "write", [id, {'id': int(id_auto), 'is_published': bool(publicado), 'active' : True,  'detailed_type' : 'consu', 'name': str(descripcion),'barcode': codigoBarra, 'categ_id': int(categoriaOdoo), 'standard_price': float(precioCosto), 'description': observaciones}])
                print("--> Se actualizo el articulo " + descripcion)



# Función encargada de ejecutar las tareas paso a paso
def main():
    # Si "op = -1" Borra un producto especificando su codigo
    # Si "op = 0" Traer todos los productos
    # Si "op = 1" Busca un artículo por código y código de barra
    # Si "op = 2" Busca un articulo por codigo de grupo por la variable codigo"

    tomarDatosArticulosSybase("1", str(118757))
    procesarArticulos(datos)
    actualizarDatosArticulos(datos)

if __name__ == "__main__":
    main()