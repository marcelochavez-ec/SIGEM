// Controla comportamientos pequenos del formulario SIGES sin mezclar JavaScript en templates.
document.addEventListener("DOMContentLoaded", () => {
    // Grupo funcional que contiene unidad y valor del tiempo de traslado.
    const grupoTiempo = document.querySelector('[data-tiempo-traslado="grupo"]');
    // Si la sección no existe en la página actual, no se ejecuta ninguna acción.
    if (!grupoTiempo) {
        return;
    }

    // Campo numérico donde se captura el tiempo de traslado.
    const campoTiempo = grupoTiempo.querySelector('[data-tiempo-traslado="valor"]');
    // Opciones de unidad: Horas o Minutos.
    const unidades = grupoTiempo.querySelectorAll('input[name="s02_am04_unidad"]');

    // Activa el campo tiempo solo cuando existe una unidad seleccionada.
    const actualizarEstadoTiempo = () => {
        // Se comprueba si alguna opción de unidad está marcada.
        const unidadSeleccionada = Array.from(unidades).find((radio) => radio.checked);
        // La existencia de una unidad marcada habilita la captura del tiempo.
        const tieneUnidad = Boolean(unidadSeleccionada);
        // El campo queda bloqueado hasta que el usuario elija Horas o Minutos.
        campoTiempo.disabled = !tieneUnidad;
        // La regla general exige valores positivos desde 1.
        campoTiempo.min = "1";
        // Horas permite decimales; minutos se ajusta mas abajo a entero.
        campoTiempo.step = "0.01";
        // Las horas no tienen maximo funcional en el formulario.
        campoTiempo.removeAttribute("max");

        if (unidadSeleccionada && unidadSeleccionada.value === "Minutos") {
            // Minutos se limita a 59 porque 60 minutos equivale a 1 hora.
            campoTiempo.max = "59";
            // Minutos se captura sin decimales.
            campoTiempo.step = "1";
            // El ejemplo visible orienta al usuario hacia minutos decimales validos.
            campoTiempo.placeholder = "Ejemplo: 15, 30 o 59";
        } else if (unidadSeleccionada && unidadSeleccionada.value === "Horas") {
            // Horas permite decimales positivos a partir de 1.
            campoTiempo.placeholder = "Ejemplo: 1, 1.65 o 2.36";
        } else {
            // El texto de ayuda visual refuerza el orden de captura.
            campoTiempo.placeholder = "Seleccione primero Horas o Minutos";
        }
    };

    // Cada cambio de unidad actualiza inmediatamente el estado del input.
    unidades.forEach((radio) => radio.addEventListener("change", actualizarEstadoTiempo));
    // Estado inicial para formularios nuevos o formularios en edición.
    actualizarEstadoTiempo();
});
