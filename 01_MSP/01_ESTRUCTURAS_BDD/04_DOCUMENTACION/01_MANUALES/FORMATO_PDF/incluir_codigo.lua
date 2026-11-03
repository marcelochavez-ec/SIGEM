-- Elaborado por: Marcelo Chávez - Consultor Especialista en Protección Social.
-- marcelo_chavez_s@outlook.com | 0983332687
-- https://www.linkedin.com/in/marcelochavezec
-- Incluye solo fuentes públicas autorizadas; nunca archivos de credenciales.
local permitidos = {
  ['deploy/presidencia/api.py']=true,
  ['deploy/presidencia/auth.py']=true,
  ['deploy/presidencia/linux/servidor.py']=true,
  ['deploy/presidencia/linux/sivas-presidencia-api.service']=true,
  ['deploy/presidencia/linux/sivas-presidencia-shiny.service']=true,
  ['deploy/presidencia/linux/sivas-presidencia-exportar.service']=true,
  ['deploy/presidencia/linux/sivas-presidencia-exportar.timer']=true,
  ['deploy/presidencia/linux/nginx-proxy.conf']=true,
  ['deploy/presidencia/linux/nginx-rutas.conf']=true,
  ['deploy/presidencia/examples/shiny_windows/cliente.R']=true,
  ['deploy/presidencia/bootstrap.R']=true,
  ['deploy/presidencia/bridge.R']=true,
  ['deploy/presidencia/shiny_app.R']=true,
  ['modulos/comprobacion_api/TEST_API.R']=true,
  ['.github/workflows/presidencia-integracion.yml']=true
}
function CodeBlock(el)
  local fuente = el.attributes['fuente']
  if not fuente then return nil end
  if not permitidos[fuente] then error('Fuente no autorizada para el manual: '..fuente) end
  local base = os.getenv('QUARTO_PROJECT_DIR') or '.'
  local archivo = assert(io.open(base..'/../../../'..fuente, 'r'))
  local lineas = {}
  for linea in archivo:lines() do table.insert(lineas, (linea:gsub('\r$', ''))) end
  archivo:close()
  local desde = tonumber(el.attributes['desde']) or 1
  local hasta = tonumber(el.attributes['hasta']) or #lineas
  assert(desde >= 1 and hasta <= #lineas and desde <= hasta, 'Rango de código inválido: '..fuente)
  local texto = {}
  for i=desde,hasta do table.insert(texto, lineas[i]) end
  el.text = table.concat(texto, '\n')
  el.attributes['fuente'] = nil
  el.attributes['desde'] = nil
  el.attributes['hasta'] = nil
  el.attributes['startFrom'] = tostring(desde)
  table.insert(el.classes, 'numberLines')
  if fuente:match('%.py$') then
    local datos = assert(io.open(base..'/recursos/explicaciones_python.json','r'))
    local notas = quarto.json.decode(datos:read('*a'))
    datos:close()
    assert(notas[fuente], 'Faltan explicaciones de '..fuente)
    local filas = {'| Línea | Explicación |','|---:|---|'}
    for i=desde,hasta do
      if lineas[i]:match('%S') then
        local nota = notas[fuente][tostring(i)]
        assert(nota and nota.codigo==lineas[i], 'Explicación desactualizada: '..fuente..':'..i)
        table.insert(filas, '| '..i..' | '..nota.explicacion:gsub('|','\\|'):gsub('\n',' ')..' |')
      end
    end
    local tabla = pandoc.read(table.concat(filas,'\n'),'markdown').blocks[1]
    tabla.colspecs = {{pandoc.AlignRight,0.08},{pandoc.AlignLeft,0.92}}
    return {el, pandoc.Para({pandoc.Strong({pandoc.Str('Lectura línea por línea: '..fuente)})}), tabla}
  end
  return el
end
function Table(el)
  local encabezado = pandoc.utils.stringify(el.head)
  if encabezado:match('Línea') and encabezado:match('Explicación') and #el.colspecs == 2 then
    el.colspecs = {{pandoc.AlignRight, 0.08}, {pandoc.AlignLeft, 0.92}}
  elseif encabezado:match('Elemento') and encabezado:match('Función en la integración') and #el.colspecs == 3 then
    el.colspecs = {{pandoc.AlignLeft, 0.13}, {pandoc.AlignLeft, 0.28}, {pandoc.AlignLeft, 0.59}}
  end
  return el
end
