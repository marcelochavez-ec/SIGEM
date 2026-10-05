// Controla comportamientos pequenos del formulario SIGES sin mezclar JavaScript en templates.
document.addEventListener("DOMContentLoaded", () => {
    // Grupo funcional que contiene unidad y valor del tiempo de traslado.
    const grupoTiempo = document.querySelector('[data-tiempo-traslado="grupo"]');
    // Si la seccion no existe en la pagina actual, no se ejecuta ninguna accion.
    if (!grupoTiempo) {
        return;
    }

    // Campo numerico donde se captura el tiempo de traslado.
    const campoTiempo = grupoTiempo.querySelector('[data-tiempo-traslado="valor"]');
    // Opciones de unidad: Horas o Minutos.
    const unidades = grupoTiempo.querySelectorAll('input[name="s02_am04_unidad"]');

    // Activa el campo tiempo solo cuando existe una unidad seleccionada.
    const actualizarEstadoTiempo = () => {
        // Se comprueba si alguna opcion de unidad esta marcada.
        const tieneUnidad = Array.from(unidades).some((radio) => radio.checked);
        // El campo queda bloqueado hasta que el usuario elija Horas o Minutos.
        campoTiempo.disabled = !tieneUnidad;
        // El texto de ayuda visual refuerza el orden de captura.
        campoTiempo.placeholder = tieneUnidad ? "Ingrese el tiempo de traslado" : "Seleccione primero Horas o Minutos";
    };

    // Cada cambio de unidad actualiza inmediatamente el estado del input.
    unidades.forEach((radio) => radio.addEventListener("change", actualizarEstadoTiempo));
    // Estado inicial para formularios nuevos o formularios en edicion.
    actualizarEstadoTiempo();
});
