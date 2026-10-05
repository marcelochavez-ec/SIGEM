# ============================================================
# Autor: Ing. Marcelo Chávez
# Consultor Especialista en Protección Social Banco Mundial
# Email: marcelo_chavez_ec@outlook.com
# ============================================================

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Count
from django.db.models import F
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import S01DatosGeneralesForm, S02AccesoMovilizacionForm
from .models import FormularioSeccion, RespuestaS01
from .models import SigesFormulario
from .services import buscar_establecimientos, guardar_matriz_siges, obtener_datos_establecimiento


"""Vistas y controladores HTTP del aplicativo SIGES.

En Django, este archivo cumple la funcion de controlador dentro del patron
MVT/MVC: recibe peticiones, coordina formularios y servicios, y devuelve
templates HTML o respuestas JSON.
"""


# Diccionario central de pasos disponibles del formulario secuencial.
PASOS = {
    "s01": {
        "orden": 1,
        "codigo": "S01",
        "nombre": "Datos Generales",
    },
    "s02": {
        "orden": 2,
        "codigo": "S02",
        "nombre": "Acceso y Movilizacion",
    },
}


def obtener_pasos_formulario():
    """Obtiene nombres de secciones desde la tabla de parametrizacion."""
    # Se copia la estructura base para conservar rutas internas del wizard.
    pasos = {clave: valor.copy() for clave, valor in PASOS.items()}
    # Se leen secciones activas desde la base para mostrar etiquetas funcionales.
    secciones = FormularioSeccion.objects.filter(codigo__in=["s01", "s02"], activo=True)
    # Se indexan por codigo en minusculas para empatar con las claves internas.
    secciones_por_codigo = {seccion.codigo.lower(): seccion for seccion in secciones}

    for clave, paso in pasos.items():
        # Si la seccion existe en base, su nombre visible reemplaza el valor de respaldo.
        seccion = secciones_por_codigo.get(clave)
        if seccion:
            paso["nombre"] = seccion.nombre
            paso["descripcion"] = seccion.descripcion

    return pasos


def health(request):
    """Devuelve estado basico del aplicativo para diagnostico."""
    return JsonResponse({"status": "ok", "app": "siges"})


def api_buscar_establecimientos(request):
    """Endpoint JSON usado por el autocompletado de establecimientos."""
    # Se lee el parametro `q` enviado por JavaScript.
    termino = request.GET.get("q", "")
    # Se lee el nivel seleccionado para limitar la busqueda de unicodigos.
    nivel_atencion = request.GET.get("nivel_atencion", "")
    # La consulta real se delega a services.py para mantener la vista simple.
    return JsonResponse({"resultados": buscar_establecimientos(termino, nivel_atencion=nivel_atencion)})


def api_detalle_establecimiento(request, unicodigo):
    """Endpoint JSON que devuelve datos S01 para un unicodigo especifico."""
    # Se conserva el filtro de nivel para evitar autocompletar establecimientos de otro formulario.
    nivel_atencion = request.GET.get("nivel_atencion", "")
    # Se busca el establecimiento en PostgreSQL por unicodigo.
    datos = obtener_datos_establecimiento(unicodigo, nivel_atencion=nivel_atencion)
    # Si no existe, se responde 404 sin lanzar traceback al navegador.
    if not datos:
        return JsonResponse({"error": "No se encontro el establecimiento."}, status=404)
    # Si existe, se entrega como objeto JSON para autocompletar el formulario.
    return JsonResponse({"establecimiento": datos})


def clave_borrador(request, pk=None):
    """Construye la llave de sesion usada para conservar avances S01/S02."""
    # Si existe pk, el borrador pertenece a una matriz en edicion.
    sufijo = str(pk) if pk else "nuevo"
    # La clave queda aislada por formulario para no mezclar capturas.
    return f"siges_matriz_local_{sufijo}"


def datos_iniciales(instancia):
    """Extrae datos existentes de una matriz para inicializar formularios."""
    # Diccionario que Django Forms usara como initial.
    inicial = {"nivel_atencion": instancia.nivel_atencion}
    # getattr evita errores si aun no existe la relacion S01.
    respuesta_s01 = getattr(instancia, "respuesta_s01", None)
    # getattr evita errores si aun no existe la relacion S02.
    respuesta_s02 = getattr(instancia, "respuesta_s02", None)

    if respuesta_s01:
        # Copia todos los campos S01 con patron s01_dg01...s01_dg13.
        for campo in [f"s01_dg{i:02d}" for i in range(1, 14)]:
            inicial[campo] = getattr(respuesta_s01, campo)

    if respuesta_s02:
        # Copia los campos S02 desde las respuestas guardadas.
        inicial.update(
            {
                "s02_am01": respuesta_s02.s02_am01,
                "s02_am02": respuesta_s02.s02_am02_id,
                "s02_am03": respuesta_s02.s02_am03_id,
                "s02_am04": respuesta_s02.s02_am04,
                "s02_am04_unidad": respuesta_s02.s02_am04_unidad,
                "s02_am05": respuesta_s02.s02_am05,
                "s02_am06": respuesta_s02.s02_am06_id,
            }
        )

    return inicial


def inicio(request):
    """Renderiza el home inicial del aplicativo."""
    return render(request, "siges/inicio.html", {"active_page": "inicio"})


def establecimientos(request):
    """Renderiza gestion de establecimientos y listado de matrices SIGES."""
    if request.method == "POST":
        ids = request.POST.getlist("seleccionados")
        accion = request.POST.get("accion", "")

        if not ids:
            messages.warning(request, "Seleccione al menos un registro para continuar.")
            return redirect("siges:establecimientos")

        if accion == "eliminar":
            seleccionados = SigesFormulario.objects.filter(pk__in=ids)
            total = seleccionados.count()
            seleccionados.delete()
            messages.success(request, f"Se eliminaron {total} matrices seleccionadas.")
            return redirect("siges:establecimientos")

        if accion == "editar" and len(ids) == 1:
            return redirect("siges:editar_matriz", pk=ids[0])

        if accion == "editar":
            messages.warning(request, "Seleccione un solo registro para modificar.")
            return redirect("siges:establecimientos")

    # Parametro de busqueda parcial por unicodigo.
    busqueda = request.GET.get("q", "").strip()
    # Parametro exacto por unicodigo.
    unicodigo = request.GET.get("unicodigo", "").strip()
    # QuerySet base de formularios.
    formularios = SigesFormulario.objects.all()
    # Filtro exacto si el usuario proporciona unicodigo completo.
    if unicodigo:
        formularios = formularios.filter(unicodigo=unicodigo)
    # Filtro parcial si el usuario proporciona texto de busqueda.
    if busqueda:
        formularios = formularios.filter(unicodigo__icontains=busqueda)

    # Se limita la salida a 20 registros para mantener la pantalla ligera.
    return render(
        request,
        "siges/establecimientos.html",
        {
            "formularios": formularios[:20],
            "busqueda": busqueda,
            "unicodigo_seleccionado": unicodigo,
            "active_page": "establecimientos",
        },
    )


def roles_usuarios(request):
    """Renderiza la pantalla visual de accesos a roles y usuarios."""
    # Se obtiene el modelo activo de usuarios definido por Django.
    User = get_user_model()
    # Se cuenta el total de usuarios para el resumen del modulo.
    total_usuarios = User.objects.count()
    # Se cuenta el total de usuarios activos para monitorear cuentas habilitadas.
    usuarios_activos = User.objects.filter(is_active=True).count()
    # Se cuenta el total de roles/grupos definidos en Django.
    total_roles = Group.objects.count()
    # Se listan usuarios recientes para dar contexto operativo sin abrir el admin.
    usuarios_recientes = User.objects.order_by("-date_joined")[:5]
    # Se listan roles alfabeticamente para mostrar la estructura de permisos disponible.
    roles_disponibles = Group.objects.order_by("name")[:5]

    return render(
        request,
        "siges/roles_usuarios.html",
        {
            "active_page": "roles",
            "total_usuarios": total_usuarios,
            "usuarios_activos": usuarios_activos,
            "total_roles": total_roles,
            "usuarios_recientes": usuarios_recientes,
            "roles_disponibles": roles_disponibles,
        },
    )


def obtener_series_reportes_monitoreo():
    """Construye indicadores y series para el dashboard de monitoreo."""
    # Total de matrices registradas en la cabecera SIGES.
    total_matrices = SigesFormulario.objects.count()
    # Total de direcciones provinciales distintas cargadas desde S01.
    total_direcciones = (
        RespuestaS01.objects.exclude(s01_dg05__isnull=True)
        .exclude(s01_dg05="")
        .values("s01_dg05")
        .distinct()
        .count()
    )
    # Archivos finales cargados: formularios enviados o validados.
    archivos_finales = SigesFormulario.objects.filter(estado__in=["ENVIADO", "VALIDADO"]).count()
    # Modificaciones: registros cuya fecha de actualizacion supera la fecha de registro.
    modificaciones = SigesFormulario.objects.filter(fecha_actualizacion__gt=F("fecha_registro")).count()
    # Versionados: formularios que ya pasaron de su primera version operativa.
    versionados = SigesFormulario.objects.filter(version__gt=1).count()

    def serie_respuesta(campo, limite=8):
        """Agrupa respuestas S01 por campo geografico o institucional."""
        # Se filtran valores vacios para no contaminar el grafico con categorias sin etiqueta.
        queryset = RespuestaS01.objects.exclude(**{f"{campo}__isnull": True}).exclude(**{campo: ""})
        # Se agrupa por el campo recibido y se cuentan unicodigos distintos.
        filas = (
            queryset.values(campo)
            .annotate(total=Count("formulario__unicodigo", distinct=True))
            .order_by("-total", campo)[:limite]
        )
        # El template y JavaScript consumen una estructura simple etiqueta/total.
        return [{"label": fila[campo], "value": fila["total"]} for fila in filas]

    # Estado de carga: lectura funcional mas clara para monitoreo ejecutivo.
    estado_carga = [
        {"label": "Almacenados", "value": total_matrices},
        {"label": "Modificados", "value": modificaciones},
        {"label": "Versionados", "value": versionados},
    ]
    # Evolucion por fecha de carga de registros.
    avance_fechas = [
        {
            "label": fila["fecha"].strftime("%Y-%m-%d") if fila["fecha"] else "Sin fecha",
            "value": fila["total"],
        }
        for fila in (
            SigesFormulario.objects.annotate(fecha=TruncDate("fecha_registro"))
            .values("fecha")
            .annotate(total=Count("id_formulario"))
            .order_by("fecha")
        )
    ]

    return {
        "metricas": {
            "total_matrices": total_matrices,
            "total_direcciones": total_direcciones,
            "archivos_finales": archivos_finales,
            "modificaciones": modificaciones,
        },
        "provincias": serie_respuesta("s01_dg05", 10),
        "estado_carga": estado_carga,
        "avance_fechas": avance_fechas,
    }


def reportes_monitoreo(request):
    """Renderiza el dashboard de reportes de monitoreo."""
    # Se preparan series compactas desde ORM para evitar logica SQL en el template.
    datos = obtener_series_reportes_monitoreo()
    # El contexto incluye datos crudos y JSON para graficacion en navegador.
    return render(
        request,
        "siges/reportes_monitoreo.html",
        {
            "active_page": "reportes",
            "datos": datos,
            "datos_json": datos,
        },
    )


def manual_usuario(request):
    """Renderiza la pantalla de manual de usuario en construccion."""
    return render(request, "siges/manual_usuario.html", {"active_page": "manual"})


def nueva_matriz(request):
    """Inicia el wizard para crear una matriz nueva."""
    return matriz_wizard(request)


def editar_matriz(request, pk):
    """Inicia el wizard sobre una matriz existente."""
    # Se obtiene la matriz o se responde 404 si el identificador no existe.
    instancia = get_object_or_404(SigesFormulario, pk=pk)
    return matriz_wizard(request, instancia=instancia)


def matriz_wizard(request, instancia=None):
    """Controla el flujo secuencial S01/S02 de la matriz SIGES."""
    # Los nombres visibles se leen desde formulario_seccion para no mostrar codigos tecnicos.
    pasos_visibles = obtener_pasos_formulario()
    # El paso se recibe por query string; si no llega, inicia en S01.
    paso = request.GET.get("paso", "s01")
    # Cualquier paso desconocido se normaliza a S01 para evitar rutas invalidas.
    if paso not in PASOS:
        paso = "s01"

    # pk permite diferenciar creacion de edicion.
    pk = instancia.pk if instancia else None
    # session_key identifica el borrador temporal en la sesion del navegador.
    session_key = clave_borrador(request, pk)
    # borrador contiene datos S01/S02 aun no persistidos definitivamente.
    borrador = request.session.get(session_key, {})
    # inicial recupera datos ya guardados cuando se edita una matriz.
    inicial = datos_iniciales(instancia) if instancia else {}

    # Para una matriz nueva, S02 queda bloqueada hasta completar S01.
    if paso == "s02" and "s01" not in borrador and not instancia:
        messages.warning(request, f"Complete {pasos_visibles['s01']['nombre']} antes de continuar.")
        return redirect(f"{reverse('siges:nueva_matriz')}?paso=s01")

    if paso == "s01":
        # Se mezclan datos guardados y borrador local para precargar el formulario.
        initial = {**inicial, **borrador.get("s01", {})}
        # En POST se valida lo enviado; en GET se muestran datos iniciales.
        form = S01DatosGeneralesForm(
            request.POST or None,
            initial=None if request.method == "POST" else initial,
        )
        # Si S01 valida, se guarda temporalmente en sesion y se avanza a S02.
        if request.method == "POST" and form.is_valid():
            borrador["s01"] = form.cleaned_data
            request.session[session_key] = borrador
            request.session.modified = True
            # La URL destino depende de si se crea o edita una matriz.
            destino = reverse("siges:editar_matriz", args=[instancia.pk]) if instancia else reverse("siges:nueva_matriz")
            return redirect(f"{destino}?paso=s02")

    else:
        # Se precarga S02 con datos guardados o con borrador de sesion.
        initial = {**inicial, **borrador.get("s02", {})}
        form = S02AccesoMovilizacionForm(
            request.POST or None,
            initial=None if request.method == "POST" else initial,
        )
        # Si S02 valida, se combina con S01 y se persiste la matriz.
        if request.method == "POST" and form.is_valid():
            # Para edicion puede no existir S01 en sesion; se recupera desde base.
            s01_data = borrador.get("s01") or {
                campo: inicial.get(campo)
                for campo in ["nivel_atencion"] + [f"s01_dg{i:02d}" for i in range(1, 14)]
            }
            # cleaned_data consolida S01 y S02.
            cleaned_data = {**s01_data, **form.cleaned_data}
            # El guardado real se delega a services.py.
            instancia = guardar_matriz_siges(
                cleaned_data=cleaned_data,
                usuario=None,
                instancia=instancia,
            )
            # Se elimina borrador temporal porque ya se persistio.
            request.session.pop(session_key, None)
            request.session.modified = True
            # El usuario se envia al detalle de la matriz guardada.
            return redirect("siges:detalle_matriz", pk=instancia.pk)

    # URL base para construir enlaces S01/S02 en el stepper.
    destino_base = reverse("siges:editar_matriz", args=[instancia.pk]) if instancia else reverse("siges:nueva_matriz")
    return render(
        request,
        "siges/matriz_form.html",
        {
            "form": form,
            "titulo": "Editar matriz SIGES" if instancia else "Nueva matriz SIGES",
            "paso": paso,
            "pasos": pasos_visibles,
            "paso_actual": pasos_visibles[paso],
            "url_s01": f"{destino_base}?paso=s01",
            "url_s02": f"{destino_base}?paso=s02",
            # S02 se habilita si ya hay S01 en sesion o si se edita una matriz existente.
            "s02_habilitada": "s01" in borrador or bool(instancia),
            "active_page": "establecimientos",
        },
    )


def detalle_matriz(request, pk):
    """Muestra la informacion guardada de una matriz SIGES."""
    # Recupera la matriz o devuelve 404 si no existe.
    instancia = get_object_or_404(SigesFormulario, pk=pk)
    # Recupera nombres funcionales de secciones para evitar codigos tecnicos en pantalla.
    pasos_visibles = obtener_pasos_formulario()
    return render(
        request,
        "siges/matriz_detalle.html",
        {
            "registro": instancia,
            "respuesta_s01": getattr(instancia, "respuesta_s01", None),
            "respuesta_s02": getattr(instancia, "respuesta_s02", None),
            "nombre_s01": pasos_visibles["s01"]["nombre"],
            "nombre_s02": pasos_visibles["s02"]["nombre"],
            "active_page": "establecimientos",
        },
    )


