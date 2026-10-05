// ============================================================
// Autor: Ing. Marcelo Chávez
// Consultor Especialista en Protección Social Banco Mundial
// Email: marcelo_chavez_ec@outlook.com
// ============================================================

// Se configura el buscador de establecimientos institucionales.
document.addEventListener("DOMContentLoaded", () => {
    const widget = document.querySelector("[data-establecimientos-widget]");
    const inputBusqueda = document.getElementById("establecimiento-busqueda");
    const botonBusqueda = document.querySelector("[data-establecimientos-boton]");
    const resultados = document.querySelector("[data-establecimientos-resultados]");
    const campoUnicodigo = document.querySelector("[data-establecimiento-campo='unicodigo']");
    const campoNivel = document.querySelector("[data-establecimiento-campo='nivel_atencion']");

    if (!widget || !inputBusqueda || !resultados || !campoUnicodigo || !campoNivel) {
        return;
    }

    let temporizador = null;

    const limpiarResultados = () => {
        resultados.innerHTML = "";
    };

    const asignarCampo = (nombre, valor) => {
        const campo = document.querySelector(`[name="${nombre}"]`);
        if (campo) {
            campo.value = valor || "";
        }
    };

    const cargarDetalle = async (unicodigo) => {
        const nivelAtencion = campoNivel.value.trim();
        if (!nivelAtencion) {
            resultados.innerHTML = '<div class="lookup-empty">Seleccione primero el nivel de atención.</div>';
            return;
        }
        const respuesta = await fetch(
            `/api/establecimientos/${encodeURIComponent(unicodigo)}/?nivel_atencion=${encodeURIComponent(nivelAtencion)}`,
        );
        if (!respuesta.ok) {
            return;
        }

        const datos = await respuesta.json();
        const establecimiento = datos.establecimiento || {};
        Object.entries(establecimiento).forEach(([nombre, valor]) => asignarCampo(nombre, valor));
        limpiarResultados();
    };

    const crearBotonResultado = (item) => {
        const boton = document.createElement("button");
        boton.type = "button";
        boton.className = "lookup-item";
        boton.innerHTML = `
            <strong>${item.unicodigo}</strong>
            <span>${item.nombre || "Sin nombre registrado"}</span>
            <small>${item.nivel_atencion || ""} · ${item.ubicacion || ""}</small>
        `;
        boton.addEventListener("click", () => {
            campoUnicodigo.value = item.unicodigo;
            inputBusqueda.value = `${item.unicodigo} - ${item.nombre || ""}`;
            cargarDetalle(item.unicodigo);
        });
        return boton;
    };

    const buscar = async () => {
        const termino = inputBusqueda.value.trim();
        const nivelAtencion = campoNivel.value.trim();
        limpiarResultados();
        if (!nivelAtencion) {
            resultados.innerHTML = '<div class="lookup-empty">Seleccione primero el nivel de atención.</div>';
            return;
        }
        if (termino.length < 2) {
            resultados.innerHTML = '<div class="lookup-empty">Escriba al menos 2 caracteres para buscar.</div>';
            return;
        }

        resultados.innerHTML = '<div class="lookup-empty">Buscando establecimientos...</div>';
        const respuesta = await fetch(
            `/api/establecimientos/buscar/?q=${encodeURIComponent(termino)}&nivel_atencion=${encodeURIComponent(nivelAtencion)}`,
        );
        limpiarResultados();
        if (!respuesta.ok) {
            resultados.innerHTML = '<div class="lookup-empty">No fue posible consultar establecimientos.</div>';
            return;
        }

        const datos = await respuesta.json();
        const lista = datos.resultados || [];
        if (!lista.length) {
            resultados.innerHTML = '<div class="lookup-empty">Sin coincidencias.</div>';
            return;
        }

        lista.forEach((item) => resultados.appendChild(crearBotonResultado(item)));
    };

    inputBusqueda.addEventListener("input", () => {
        window.clearTimeout(temporizador);
        temporizador = window.setTimeout(buscar, 280);
    });

    inputBusqueda.addEventListener("focus", () => {
        if (!inputBusqueda.value.trim()) {
            resultados.innerHTML = '<div class="lookup-empty">Escriba un unicodigo o parte del nombre del establecimiento.</div>';
        }
    });

    if (botonBusqueda) {
        botonBusqueda.addEventListener("click", buscar);
    }

    campoNivel.addEventListener("change", () => {
        campoUnicodigo.value = "";
        inputBusqueda.value = "";
        limpiarResultados();
    });

    campoUnicodigo.addEventListener("change", () => {
        if (campoUnicodigo.value.trim()) {
            cargarDetalle(campoUnicodigo.value.trim());
        }
    });
});

