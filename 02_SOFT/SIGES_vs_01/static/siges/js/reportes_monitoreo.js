(() => {
    const dataNode = document.getElementById("reportes-monitoreo-data");
    if (!dataNode) return;

    const data = JSON.parse(dataNode.textContent);
    const colors = ["#087bff", "#14b866", "#18bcc7", "#ff9800", "#7c3cff", "#ef233c", "#0056a8", "#2c9d35"];
    const chartRegions = new Map();

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

    const tooltip = document.createElement("div");
    tooltip.className = "report-tooltip";
    tooltip.hidden = true;
    document.body.appendChild(tooltip);

    const positionTooltip = (event) => {
        const gap = 14;
        const margin = 10;
        const tooltipWidth = tooltip.offsetWidth;
        const tooltipHeight = tooltip.offsetHeight;
        const rightPosition = event.clientX + gap;
        const leftPosition = event.clientX - tooltipWidth - gap;
        const topPosition = Math.min(
            Math.max(event.clientY + gap, margin),
            window.innerHeight - tooltipHeight - margin,
        );
        const finalLeft = rightPosition + tooltipWidth + margin > window.innerWidth
            ? Math.max(leftPosition, margin)
            : rightPosition;

        tooltip.style.left = `${finalLeft}px`;
        tooltip.style.top = `${topPosition}px`;
    };

    const setupCanvas = (canvas) => {
        const ratio = window.devicePixelRatio || 1;
        const width = canvas.clientWidth || canvas.parentElement.clientWidth;
        const height = Number(canvas.getAttribute("height")) || 230;
        canvas.width = width * ratio;
        canvas.height = height * ratio;
        const ctx = canvas.getContext("2d");
        ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
        ctx.clearRect(0, 0, width, height);
        ctx.font = "12px 'Century Gothic', Arial, sans-serif";
        ctx.textBaseline = "middle";
        chartRegions.set(canvas.id, []);
        return { ctx, width, height };
    };

    const addRegion = (canvasId, region) => {
        const regions = chartRegions.get(canvasId) || [];
        regions.push(region);
        chartRegions.set(canvasId, regions);
    };

    const emptyChart = (ctx, width, height) => {
        ctx.fillStyle = "#536da6";
        ctx.textAlign = "center";
        ctx.fillText("Sin datos disponibles", width / 2, height / 2);
    };

    const wrapLabel = (ctx, text, maxWidth) => {
        const words = String(text || "Sin etiqueta").split(/\s+/);
        const lines = [];
        let currentLine = "";

        words.forEach((word) => {
            const nextLine = currentLine ? `${currentLine} ${word}` : word;
            if (ctx.measureText(nextLine).width <= maxWidth || !currentLine) {
                currentLine = nextLine;
                return;
            }
            lines.push(currentLine);
            currentLine = word;
        });

        if (currentLine) lines.push(currentLine);
        return lines;
    };

    const drawBars = (canvasId, rows) => {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const { ctx, width, height } = setupCanvas(canvas);
        if (!rows.length) return emptyChart(ctx, width, height);

        const maxValue = Math.max(...rows.map((row) => row.value), 1);
        const labelWidth = Math.min(310, Math.max(190, width * .34));
        const left = labelWidth + 18;
        const top = 12;
        const rowHeight = Math.max(48, (height - 24) / rows.length);

        rows.forEach((row, index) => {
            const y = top + index * rowHeight;
            const barWidth = Math.max(4, ((width - left - 28) * row.value) / maxValue);
            const barHeight = rowHeight - 10;
            const label = String(row.label || "Sin etiqueta");
            const labelLines = wrapLabel(ctx, label, labelWidth);
            const lineHeight = 13;
            const labelStartY = y + rowHeight / 2 - ((labelLines.length - 1) * lineHeight) / 2;

            ctx.fillStyle = "#17336e";
            ctx.textAlign = "left";
            labelLines.forEach((line, lineIndex) => {
                ctx.fillText(line, 0, labelStartY + lineIndex * lineHeight);
            });
            ctx.fillStyle = colors[index % colors.length];
            ctx.shadowColor = "rgba(0, 65, 180, .18)";
            ctx.shadowBlur = 8;
            ctx.fillRect(left, y + 5, barWidth, barHeight);
            ctx.shadowBlur = 0;
            ctx.fillStyle = "#07118f";
            ctx.textAlign = "left";
            ctx.fillText(row.value, left + barWidth + 8, y + rowHeight / 2);

            addRegion(canvasId, {
                type: "rect",
                x: left,
                y: y + 5,
                width: barWidth,
                height: barHeight,
                title: "Dirección Provincial",
                body: `${label}: ${row.value} matrices registradas.`,
            });
        });
    };

    const drawDonut = (canvasId, rows) => {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const { ctx, width, height } = setupCanvas(canvas);
        if (!rows.length) return emptyChart(ctx, width, height);

        const total = rows.reduce((sum, row) => sum + row.value, 0) || 1;
        const centerX = Math.min(width * .36, 126);
        const centerY = height / 2;
        const radius = Math.min(height * .34, 72);
        let start = -Math.PI / 2;

        rows.forEach((row, index) => {
            const angle = (row.value / total) * Math.PI * 2;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, start, start + angle);
            ctx.closePath();
            ctx.fillStyle = colors[index % colors.length];
            ctx.fill();
            addRegion(canvasId, {
                type: "arc",
                cx: centerX,
                cy: centerY,
                inner: radius * .58,
                outer: radius,
                start,
                end: start + angle,
                title: "Estado de Carga",
                body: `${row.label}: ${row.value} matrices.`,
            });
            start += angle;
        });

        ctx.globalCompositeOperation = "destination-out";
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * .58, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalCompositeOperation = "source-over";

        ctx.fillStyle = "#07118f";
        ctx.textAlign = "center";
        ctx.font = "700 17px 'Century Gothic', Arial, sans-serif";
        ctx.fillText(total, centerX, centerY);

        rows.slice(0, 5).forEach((row, index) => {
            const x = centerX + radius + 24;
            const y = 38 + index * 25;
            ctx.fillStyle = colors[index % colors.length];
            ctx.fillRect(x, y - 6, 12, 12);
            ctx.fillStyle = "#17336e";
            ctx.textAlign = "left";
            ctx.font = "12px 'Century Gothic', Arial, sans-serif";
            ctx.fillText(`${row.label}: ${row.value}`, x + 18, y);
        });
    };

    const drawLine = (canvasId, rows) => {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const { ctx, width, height } = setupCanvas(canvas);
        if (!rows.length) return emptyChart(ctx, width, height);

        const padding = 34;
        const maxValue = Math.max(...rows.map((row) => row.value), 1);
        const stepX = rows.length > 1 ? (width - padding * 2) / (rows.length - 1) : 0;
        const points = rows.map((row, index) => ({
            x: padding + index * stepX,
            y: height - padding - ((height - padding * 2) * row.value) / maxValue,
            label: row.label,
            value: row.value,
        }));

        ctx.strokeStyle = "#d9f1ff";
        ctx.lineWidth = 1;
        for (let i = 0; i < 4; i += 1) {
            const y = padding + i * ((height - padding * 2) / 3);
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(width - padding, y);
            ctx.stroke();
        }

        ctx.strokeStyle = "#087bff";
        ctx.lineWidth = 4;
        ctx.lineJoin = "round";
        ctx.beginPath();
        points.forEach((point, index) => {
            if (index === 0) ctx.moveTo(point.x, point.y);
            else ctx.lineTo(point.x, point.y);
        });
        ctx.stroke();

        points.forEach((point) => {
            ctx.fillStyle = "#ffffff";
            ctx.beginPath();
            ctx.arc(point.x, point.y, 7, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#087bff";
            ctx.lineWidth = 3;
            ctx.stroke();
            ctx.fillStyle = "#07118f";
            ctx.textAlign = "center";
            ctx.font = "700 12px 'Century Gothic', Arial, sans-serif";
            ctx.fillText(point.value, point.x, point.y - 18);
            ctx.font = "11px 'Century Gothic', Arial, sans-serif";
            ctx.fillText(point.label.slice(5), point.x, height - 12);

            addRegion(canvasId, {
                type: "circle",
                x: point.x,
                y: point.y,
                radius: 12,
                title: "Fecha de Carga",
                body: `${point.label}: ${point.value} matrices registradas.`,
            });
        });
    };

    const hitRegion = (canvas, event) => {
        const rect = canvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        return (chartRegions.get(canvas.id) || []).find((region) => {
            if (region.type === "rect") {
                return x >= region.x && x <= region.x + region.width && y >= region.y && y <= region.y + region.height;
            }
            if (region.type === "circle") {
                return Math.hypot(x - region.x, y - region.y) <= region.radius;
            }
            if (region.type === "arc") {
                const distance = Math.hypot(x - region.cx, y - region.cy);
                let angle = Math.atan2(y - region.cy, x - region.cx);
                if (angle < -Math.PI / 2) angle += Math.PI * 2;
                return distance >= region.inner && distance <= region.outer && angle >= region.start && angle <= region.end;
            }
            return false;
        });
    };

    const bindCanvasEvents = () => {
        document.querySelectorAll(".report-chart").forEach((canvas) => {
            canvas.onmousemove = (event) => {
                const region = hitRegion(canvas, event);
                canvas.style.cursor = region ? "pointer" : "default";
                if (!region) {
                    tooltip.hidden = true;
                    return;
                }
                tooltip.textContent = region.body;
                tooltip.hidden = false;
                positionTooltip(event);
            };
            canvas.onmouseleave = () => {
                tooltip.hidden = true;
                canvas.style.cursor = "default";
            };
            canvas.onclick = (event) => {
                const region = hitRegion(canvas, event);
                if (region) showPopup(region.title, region.body);
            };
        });
    };

    const drawAll = () => {
        drawBars("chartProvincias", data.provincias || []);
        drawDonut("chartEstados", data.estado_carga || []);
        drawLine("chartAvance", data.avance_fechas || []);
        bindCanvasEvents();
    };

    drawAll();
    window.addEventListener("resize", drawAll);
})();

