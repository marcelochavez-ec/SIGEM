(() => {
    const dataNode = document.getElementById("reportes-monitoreo-data");
    if (!dataNode || typeof echarts === "undefined") return;

    const data = JSON.parse(dataNode.textContent);
    const charts = [];
    const colors = ["#087bff", "#14b866", "#18bcc7", "#ff9800", "#7c3cff", "#ef233c", "#0056a8", "#2c9d35"];
    const fontFamily = "'Century Gothic', Arial, sans-serif";

    const popup = {
        panel: document.querySelector("[data-report-popup-panel]"),
        title: document.querySelector("[data-report-popup-title]"),
        body: document.querySelector("[data-report-popup-body]"),
        close: document.querySelector("[data-report-popup-close]"),
    };

    const showPopup = (title, body) => {
        if (!popup.panel || !popup.title || !popup.body) return;
        popup.title.textContent = title;
        popup.body.textContent = body;
        popup.panel.hidden = false;
    };

    const hidePopup = () => {
        if (popup.panel) popup.panel.hidden = true;
    };

    if (popup.close) popup.close.addEventListener("click", hidePopup);
    if (popup.panel) {
        popup.panel.addEventListener("click", (event) => {
            if (event.target === popup.panel) hidePopup();
        });
    }

    document.querySelectorAll("[data-report-popup]").forEach((element) => {
        element.addEventListener("click", () => {
            const [title, body] = element.dataset.reportPopup.split("|");
            showPopup(title, body);
        });
    });

    const tooltip = {
        trigger: "item",
        appendToBody: true,
        confine: true,
        backgroundColor: "#ffffff",
        borderColor: "#bfe7ff",
        borderWidth: 1,
        borderRadius: 8,
        padding: [9, 11],
        textStyle: {
            color: "#07118f",
            fontFamily,
            fontSize: 12,
        },
        extraCssText: "box-shadow:0 14px 30px rgba(0,65,180,.18);",
    };

    const chartBase = {
        color: colors,
        textStyle: {
            color: "#17336e",
            fontFamily,
        },
        animationDuration: 650,
        animationEasing: "cubicOut",
    };

    const initChart = (id) => {
        const element = document.getElementById(id);
        if (!element) return null;
        const chart = echarts.init(element, null, { renderer: "canvas" });
        charts.push(chart);
        return chart;
    };

    const renderEmpty = (chart) => {
        chart.setOption({
            ...chartBase,
            title: {
                text: "Sin datos disponibles",
                left: "center",
                top: "middle",
                textStyle: {
                    color: "#536da6",
                    fontFamily,
                    fontSize: 13,
                    fontWeight: 500,
                },
            },
        });
    };

    const renderProvincias = () => {
        const chart = initChart("chartProvincias");
        if (!chart) return;
        const rows = data.provincias || [];
        if (!rows.length) return renderEmpty(chart);

        chart.setOption({
            ...chartBase,
            grid: { left: 8, right: 34, top: 10, bottom: 8, containLabel: true },
            tooltip: {
                ...tooltip,
                formatter: (params) => `${params.name}<br><strong>${params.value}</strong> matrices registradas`,
            },
            xAxis: {
                type: "value",
                axisLine: { show: false },
                axisTick: { show: false },
                splitLine: { lineStyle: { color: "#d9f1ff" } },
                axisLabel: { color: "#536da6", fontFamily },
            },
            yAxis: {
                type: "category",
                inverse: true,
                data: rows.map((row) => row.label),
                axisLine: { show: false },
                axisTick: { show: false },
                axisLabel: {
                    color: "#17336e",
                    fontFamily,
                    width: 210,
                    overflow: "break",
                    lineHeight: 14,
                    formatter: (value) => String(value || "Sin etiqueta"),
                },
            },
            series: [{
                name: "Matrices",
                type: "bar",
                data: rows.map((row, index) => ({
                    value: row.value,
                    itemStyle: {
                        color: colors[index % colors.length],
                        borderRadius: [0, 5, 5, 0],
                    },
                })),
                barMaxWidth: 34,
                label: {
                    show: true,
                    position: "right",
                    color: "#07118f",
                    fontFamily,
                    fontWeight: 700,
                },
                emphasis: { focus: "series" },
            }],
        });

        chart.on("click", (params) => {
            showPopup("Dirección Provincial", `${params.name}: ${params.value} matrices registradas.`);
        });
    };

    const renderEstados = () => {
        const chart = initChart("chartEstados");
        if (!chart) return;
        const rows = data.estado_carga || [];
        if (!rows.length) return renderEmpty(chart);
        const total = rows.reduce((sum, row) => sum + Number(row.value || 0), 0);

        chart.setOption({
            ...chartBase,
            tooltip: {
                ...tooltip,
                formatter: (params) => `${params.name}<br><strong>${params.value}</strong> matrices`,
            },
            legend: {
                orient: "vertical",
                right: 4,
                top: "middle",
                icon: "roundRect",
                itemWidth: 10,
                itemHeight: 10,
                textStyle: { color: "#17336e", fontFamily, fontSize: 12 },
            },
            graphic: [{
                type: "text",
                left: "24%",
                top: "center",
                style: {
                    text: String(total),
                    fill: "#07118f",
                    font: `700 18px ${fontFamily}`,
                    textAlign: "center",
                    textVerticalAlign: "middle",
                },
            }],
            series: [{
                name: "Estado de Carga",
                type: "pie",
                radius: ["46%", "68%"],
                center: ["27%", "50%"],
                avoidLabelOverlap: true,
                label: { show: false },
                labelLine: { show: false },
                data: rows.map((row) => ({ name: row.label, value: row.value })),
                emphasis: {
                    scaleSize: 8,
                    itemStyle: { shadowBlur: 18, shadowColor: "rgba(0, 65, 180, .22)" },
                },
            }],
        });

        chart.on("click", (params) => {
            showPopup("Estado de Carga", `${params.name}: ${params.value} matrices.`);
        });
    };

    const renderAvance = () => {
        const chart = initChart("chartAvance");
        if (!chart) return;
        const rows = data.avance_fechas || [];
        if (!rows.length) return renderEmpty(chart);

        chart.setOption({
            ...chartBase,
            grid: { left: 38, right: 28, top: 18, bottom: 34, containLabel: true },
            tooltip: {
                ...tooltip,
                trigger: "axis",
                axisPointer: { type: "line", lineStyle: { color: "#087bff", width: 1.5 } },
                position: (point, _params, _dom, _rect, size) => {
                    const left = point[0] + size.contentSize[0] + 22 > size.viewSize[0]
                        ? point[0] - size.contentSize[0] - 14
                        : point[0] + 14;
                    return [Math.max(left, 8), Math.max(point[1] + 10, 8)];
                },
                formatter: (params) => {
                    const item = params[0];
                    return `${item.axisValue}<br><strong>${item.value}</strong> matrices registradas`;
                },
            },
            xAxis: {
                type: "category",
                boundaryGap: false,
                data: rows.map((row) => row.label),
                axisLine: { lineStyle: { color: "#bfe7ff" } },
                axisTick: { show: false },
                axisLabel: {
                    color: "#536da6",
                    fontFamily,
                    formatter: (value) => String(value).slice(5),
                },
            },
            yAxis: {
                type: "value",
                minInterval: 1,
                axisLine: { show: false },
                axisTick: { show: false },
                splitLine: { lineStyle: { color: "#d9f1ff" } },
                axisLabel: { color: "#536da6", fontFamily },
            },
            series: [{
                name: "Matrices",
                type: "line",
                data: rows.map((row) => row.value),
                smooth: true,
                symbol: "circle",
                symbolSize: 9,
                lineStyle: { color: "#087bff", width: 4 },
                itemStyle: { color: "#087bff", borderColor: "#ffffff", borderWidth: 2 },
                areaStyle: {
                    color: {
                        type: "linear",
                        x: 0,
                        y: 0,
                        x2: 0,
                        y2: 1,
                        colorStops: [
                            { offset: 0, color: "rgba(8, 123, 255, .26)" },
                            { offset: 1, color: "rgba(8, 123, 255, 0)" },
                        ],
                    },
                },
                label: {
                    show: true,
                    position: "top",
                    color: "#07118f",
                    fontFamily,
                    fontWeight: 700,
                },
            }],
        });

        chart.on("click", (params) => {
            showPopup("Fecha de Carga", `${params.name}: ${params.value} matrices registradas.`);
        });
    };

    renderProvincias();
    renderEstados();
    renderAvance();

    window.addEventListener("resize", () => {
        charts.forEach((chart) => chart.resize());
    });
})();
