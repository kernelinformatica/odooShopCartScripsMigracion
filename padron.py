from xmlrpc import client



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

def tomarDatosPadronSybase(op, codigo):
    # deberia implementar algun token de seguridad en estas consultas, despúes se vera cual es la mejor manera.
    print("Conecto con Sybase para traer el padron :::: "+op)
    print("Aguarde un momento por favor ...")
    import conn.sybase
    global datos
    cursor = conn.sybase.conn.cursor()

    if op == "1":
        # Trae padron por codigo padron


            cursor.execute("select id, padron_apelli, padron_nombre, 1 as codigoEmpresa, ctacte_condiva.odoo_codigo as padron_ivacon, padron_docnro,  padron_observa,  ctacte_padron.codigo_postal, 'AR' as paisCodigo, ctacte_provincia.provi_descri as provincia, ctacte_provincia.odoo_codigo as pciaCodigo, ctacte_padron.codigo_docu, ctacte_categoria.odoo_codigo as odoo_catego, "
            "ctacte_localidad.loc_localidad  as ciudad, padron_domici, padron_domnro, padron_codigo, padron_telcar, padron_telnro, '0' as cel, 'sistemas@kernelinformatica.com.ar' as email, "
            "padron_cuit11, padron_cuil11,  ctacte_condiva.descripcion as ivaCondicionNombre  from ctacte_categoria, ctacte_padron, ctacte_localidad, ctacte_provincia, ctacte_condiva "
            "where padron_codigo = "+str(codigo)+ " and ctacte_localidad.codigo_postal = ctacte_padron.codigo_postal  "
            "and ctacte_provincia.codigo_provi = ctacte_localidad.codigo_provi "
            "and ctacte_categoria.padron_catego = ctacte_padron.padron_catego "
            "and ctacte_condiva.condiva = ctacte_padron.padron_ivacon")
    elif op == "-1":

        cursor.execute("select id, padron_apelli, padron_nombre, 1 as codigoEmpresa, ctacte_condiva.odoo_codigo as padron_ivacon, padron_docnro, padron_observa,  ctacte_padron.codigo_postal, 'AR' as paisCodigo, ctacte_provincia.provi_descri as provincia, ctacte_provincia.odoo_codigo as pciaCodigo, codigo_docu,  ctacte_categoria.odoo_codigo as odoo_catego,"
            "ctacte_localidad.loc_localidad  as ciudad, padron_domici, padron_domnro, padron_codigo, padron_telcar, padron_telnro, '0' as cel, 'sistemas@kernelinformatica.com.ar' as email, "
            "padron_cuit11, padron_cuil11 , ctacte_condiva.descripcion as ivaCondicionNombre from ctacte_categoria, ctacte_padron, ctacte_localidad, ctacte_provincia , ctacte_condiva "
            "where ctacte_padron.padron_codigo = "+str(codigo)+ " and ctacte_localidad.codigo_postal = ctacte_padron.codigo_postal"
            " and ctacte_provincia.codigo_provi = ctacte_localidad.codigo_provi "
            "and ctacte_categoria.padron_catego = ctacte_padron.padron_catego"
            "and ctacte_condiva.condiva = ctacte_padron.padron_ivacon ")
    elif op == "2":
        # Trae el pádron por categoria
        if codigo == 0:
            condicionCategoria = ""
        else:
            condicionCategoria = " and padron_catego = "+str(codigo)

        cursor.execute( "select id, padron_apelli, padron_nombre, 1 as codigoEmpresa, ctacte_condiva.odoo_codigo as padron_ivacon, padron_docnro, padron_observa,  ctacte_categoria.odoo_codigo as odoo_catego, "
                        "ctacte_padron.codigo_postal, 'AR' as paisCodigo, ctacte_provincia.provi_descri as provincia, ctacte_provincia.odoo_codigo as pciaCodigo, codigo_docu,  "
        "ctacte_localidad.loc_localidad  as ciudad, padron_domici, padron_domnro, padron_codigo, padron_telcar, padron_telnro, '0' as cel, 'sistemas@kernelinformatica.com.ar' as email, "
        "padron_cuit11, padron_cuil11 , ctacte_condiva.descripcion as ivaCondicionNombre from ctacte_categoria, ctacte_padron, ctacte_localidad, ctacte_provincia , ctacte_condiva "
        "where ctacte_localidad.codigo_postal = ctacte_padron.codigo_postal"
         "and ctacte_categoria.padron_catego = ctacte_padron.padron_catego"
        " and ctacte_provincia.codigo_provi = ctacte_localidad.codigo_provi "
        "and ctacte_condiva.condiva = ctacte_padron.padron_ivacon "
        "and  padron_catego > 0 " + condicionCategoria + "")

    elif op == "0":

        cursor.execute(
        "select id, padron_apelli, padron_nombre, 1 as codigoEmpresa, ctacte_condiva.odoo_codigo as padron_ivacon, padron_docnro, padron_observa,  ctacte_padron.codigo_postal, 'AR' as paisCodigo, ctacte_provincia.provi_descri as provincia, ctacte_provincia.odoo_codigo as pciaCodigo, codigo_docu, ctacte_categoria.odoo_codigo as odoo_catego "
        "ctacte_localidad.loc_localidad  as ciudad, padron_domici, padron_domnro, padron_codigo, padron_telcar, padron_telnro, '0' as cel, 'sistemas@kernelinformatica.com.ar' as email, "
        "padron_cuit11, padron_cuil11  from ctacte_categoria, ctacte_padron, ctacte_localidad, ctacte_provincia, ctacte_condiva "
        "where ctacte_localidad.codigo_postal = ctacte_padron.codigo_postal"
        "and ctacte_condiva.condiva = ctacte_padron.padron_ivacon "
        "and ctacte_categoria.padron_catego = ctacte_padron.padron_catego"
        "and  ctacte_padron.padron_catego > 0 "
        "and ctacte_provincia.codigo_provi = ctacte_localidad.codigo_provi ")

    padron = cursor.fetchall()
    if len(padron) > 0:
        for p in padron:

            abm = op
            id_auto = p.id
            codigoPadron = p.padron_codigo

            telefono = str(p.padron_telcar)+" "+str(p.padron_telnro)
            if p.padron_nombre == None:
                nombreApellido = p.padron_apelli
            else:
                nombreApellido = p.padron_apelli +" "+p.padron_nombre
                codigoEmpresa = p.codigoEmpresa
                codigoPostal = p.codigo_postal
                codigoPais = p.paisCodigo
                codigoPcia = p.pciaCodigo
                codigoCiudad = p.ciudad
                if p.padron_domnro == None:
                  domicilio = str(p.padron_domici)
                else:
                  domicilio  = str(p.padron_domici) +" "+str(p.padron_domnro)

            codigoDocu=  p.codigo_docu
            nroDocu = p.padron_docnro
            ivaCondicion = p.padron_ivacon
            padronCategoria = p.odoo_catego
            if padronCategoria == 0 or padronCategoria == None:
                padronCategoria = 2
            cuit = p.padron_cuit11
            cuil = p.padron_cuil11
            if ivaCondicion == 6:
                #Monotributista
                if cuil == 0:
                    cuil = cuit
                    cuitCuil =  str(cuil)
                else:
                    cuitCuil = str(cuil)
            elif ivaCondicion == 3:
                cuitCuil = str(cuit)
            elif ivaCondicion == 4:
                #Extento
                cuitCuil = ''

            elif ivaCondicion == 5:
                # Consumidor Final
                if len(str(nroDocu)) == 8:
                    cuitCuil = nroDocu
                else:
                    cuitCuil = ''


            else:

                if len(str(cuit)) == 11:
                    cuitCuil = 'AR' + str(cuit)

                else:
                    #Si el formato es inválido lo envio como consumidor final y luego que se ajuste en otro proceso
                    cuitCuil = ""
                    ivaCondicion = 5
            if cuit == 0 and cuil == 0:
                ivaCondicion = 5
                if nroDocu == 0:
                    cuitCuil = ''
                else:
                    if len(str(nroDocu)) == 8:
                        cuitCuil = nroDocu
                    else:
                        cuitCuil = ''
                print("los dos son 0 entonces los debo setear como consumidor final por defecto --> Condicion de iva : "+str(ivaCondicion))





            observaciones = p.padron_observa
            celular = p.cel
            email = p.email
            ivaCondicionNombre = p.ivaCondicionNombre
            datos.append([abm, id_auto, codigoPadron, nombreApellido, codigoEmpresa, codigoPostal, codigoPais, codigoPcia, codigoCiudad, domicilio, codigoDocu,nroDocu, ivaCondicion, padronCategoria, cuit, cuil, cuitCuil, celular, email, domicilio, telefono, ivaCondicionNombre,  observaciones ])
            #print(f"{abm}\t{id_auto}\t{codigoPadron}\t{nombreApellido}\t{codigoEmpresa}\t{codigoPostal}\t{codigoPais}\t{codigoPcia}\t {codigoCiudad}\t {domicilio}\t{codigoDocu}\t{nroDocu}\t{ivaCondicion}\t{padronCategoria}\t{cuit}\t{cuil}\t{observaciones}")
    else:
        print("La busqueda no arrojo resultados")


# procesas los datos

def procesarPadron(datos):
    # En esta función los datos pueden ser alterados.
    datos_nuevos = []
    for abm, id_auto, codigoPadron, nombreApellido, codigoEmpresa, codigoPostal, codigoPais, codigoPcia, codigoCiudad, domicilio, codigoDocu,nroDocu, ivaCondicion, padronCategoria, cuit, cuil, cuitCuil, celular, email, domicilio, telefono, ivaCondicionNombre,observaciones in datos:
        datos_nuevos.append([abm, id_auto, codigoPadron, nombreApellido, codigoEmpresa, codigoPostal, codigoPais, codigoPcia, codigoCiudad, domicilio, codigoDocu,nroDocu, ivaCondicion, padronCategoria, cuit, cuil, cuitCuil, celular, email, domicilio, telefono, ivaCondicionNombre, observaciones])
        datos = datos_nuevos
        #print(datos)

# actualizar los datos en odoo

def actualizarDatosPadron(datos):
    for abm, id_auto, codigoPadron, nombreApellido, codigoEmpresa, codigoPostal, codigoPais, codigoPcia, codigoCiudad, domicilio, codigoDocu,nroDocu, ivaCondicion, padronCategoria, cuit, cuil, cuitCuil, celular, email, domicilio, telefono, ivaCondicionNombre, observaciones  in datos:
        # Busqueda del artículo a traves del campo nombre

        # domain = [('name','like',descripcion)]
        domain = [('street2', '=', int(codigoPadron))]
        id = api.execute_kw(db, str(uid), password, "res.partner", "search", [domain])

        if not id:
            # si el cliente no existe, crea uno nuevo
            print("--> Se agrego el padron "+nombreApellido)
            r = api.execute_kw(db, uid, password, "res.partner", "create", [{'name': nombreApellido,
                                                                                'street2': int(codigoPadron),
                                                                                'street': str(domicilio),
                                                                                'city': str(codigoCiudad),
                                                                                'state_id' : int(codigoPcia),
                                                                                'mobile': int(celular),
                                                                                'phone' : str(telefono),
                                                                                'category_id' : str(padronCategoria),
                                                                                'l10n_latam_identification_type_id' :int(ivaCondicion),
                                                                                'l10n_ar_afip_responsibility_type_id': int(ivaCondicion),
                                                                                'email' : str(email),
                                                                                'vat' : str(cuitCuil),
                                                                                'zip' : int(codigoPostal)} ])
        else:

            if abm == '-1':
              # Borra un registro del padron
              r = api.execute_kw(db, uid, password, "res.partner", "unlink", [id])
              print("--> Se borra el cliente " + nombreApellido)
            else:
                print("PADRON CATEGORIA -----> "+str(padronCategoria))
                # si el cliente existe se actualiza  '|10n_ar_afip_responsibility_type_id' : int(ivaCondicion),
                r = api.execute_kw(db, uid, password, "res.partner", "write", [id, {'name': nombreApellido,
                                                                                'street2': int(codigoPadron),
                                                                                'street': str(domicilio),
                                                                                'city': str(codigoCiudad),
                                                                                'state_id' : int(codigoPcia),
                                                                                'mobile': int(celular),
                                                                                'phone' : str(telefono),
                                                                                'category_id': [int(padronCategoria)],
                                                                                'l10n_latam_identification_type_id' : int(ivaCondicion),
                                                                                'l10n_ar_afip_responsibility_type_id': int(ivaCondicion),
                                                                                'email' : str(email),
                                                                                'vat' : str(cuitCuil),
                                                                                'zip' : int(codigoPostal)} ])
            print("--> Se actualiza el cliente " + nombreApellido)

# Función encargada de ejecutar las tareas paso a paso
def main():
    #op = 0: codigo = 0 'Procesa todo el padron'
    #op = 1, codigo = xxxxx: 'Procesa por codigo de padron'
    #op = 2, codigo = xx: Procesa por codigo de categoria'
    tomarDatosPadronSybase("1",23476)
    #tomarDatosPadronSybase("1", 2717)
    procesarPadron(datos)
    actualizarDatosPadron(datos)

if __name__ == "__main__":
    main()