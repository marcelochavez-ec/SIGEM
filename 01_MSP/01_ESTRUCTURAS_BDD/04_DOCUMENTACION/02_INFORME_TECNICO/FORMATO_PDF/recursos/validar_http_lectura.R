invisible(Sys.setlocale('LC_CTYPE','Spanish_Ecuador.utf8'))
invisible(source('modulos/comprobacion_api/TEST_API.R',encoding='UTF-8'))
args<-commandArgs(trailingOnly=TRUE)
root<-'tmp/auditoria_api_20261026'
dir.create(root,showWarnings=FALSE,recursive=TRUE)
now<-function()format(Sys.time(),tz='UTC',format='%Y-%m-%dT%H:%M:%SZ')
res<-list(inicio_utc=now(),zona_horaria='America/Guayaquil',tipo='real_197_desde_R_Windows',base=config$base,indicadores=list())
for(id in presidencia_ids_cliente){
 e<-list(id=id,inicio_utc=now(),estado='pendiente');s<-NULL
 tryCatch({
  s<-presidencia_solicitar_sesion(config,id)
  e$autenticacion<-list(estado='aprobado',enlaces=length(s$indicadores),vigencia_configurada_segundos=s$vigencia_segundos)
  data<-presidencia_http_cliente(config,paste0('/api/v1/presidencia/',id,'/serie'))
  jsonlite::write_json(data,file.path(root,paste0(id,'_rest.json')),auto_unbox=TRUE,pretty=TRUE,na='null',null='null')
  e$rest<-list(estado='aprobado',filas=length(data$datos),generado_en=data$generado_en)
  r<-httr::GET(s$indicadores[[id]],httr::timeout(20));e$envoltura<-list(http=httr::status_code(r),html=grepl('iframe',httr::content(r,as='text',encoding='UTF-8'),fixed=TRUE))
  shiny_url<-paste0(sub('/embed/presidencia$','/shiny/',s$url),'?indicador=',id)
  t<-system.time(r<-httr::GET(shiny_url,httr::timeout(30)))
  html<-httr::content(r,as='text',encoding='UTF-8')
  e$html_shiny<-list(http=httr::status_code(r),segundos=unname(t['elapsed']),bytes=nchar(html),contenedor=grepl('contenido_panel',html,fixed=TRUE),login_eliminado=!grepl('id="indicadores_presidencia-login_usuario"',html,fixed=TRUE))
  e$estado<-'aprobado'
 },error=function(err){e$estado<<-'fallido';e$error<<-gsub('/vista/[A-Za-z0-9_-]{43}','/vista/[SESION]',conditionMessage(err))})
 if(!is.null(s))tryCatch({c<-presidencia_cerrar_sesion(s,config);r<-httr::GET(s$url,httr::timeout(15));e$cierre<-list(estado=if(httr::status_code(r)==401)'aprobado'else'fallido',respuesta=c$estado,reutilizacion=httr::status_code(r))},error=function(err)e$cierre<<-list(estado='fallido',mensaje='Fallo de cierre; revisar sesión temporal.'))
 e$fin_utc<-now();res$indicadores[[id]]<-e
 cat(id,e$estado,'\n')
}
res$fin_utc<-now();jsonlite::write_json(res,file.path(root,'http_real.json'),auto_unbox=TRUE,pretty=TRUE,na='null',null='null')
