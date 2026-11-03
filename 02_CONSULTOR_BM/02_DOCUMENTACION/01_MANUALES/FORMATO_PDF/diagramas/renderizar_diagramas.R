Sys.setlocale('LC_CTYPE','Spanish_Ecuador.utf8')
# Elaborado por Marcelo Chávez. marcelo_chavez_s@outlook.com | 098 333 26 87.
# https://www.linkedin.com/in/marcelochavezec
library(chromote)
d <- normalizePath('docs/manuales/api_presidencia/diagramas',winslash='/')
b <- ChromoteSession$new()
tryCatch({
 for(n in c('arquitectura','secuencia','seguridad','concurrencia')) {
  svg <- paste(readLines(file.path(d,paste0(n,'.svg')),encoding='UTF-8',warn=FALSE),collapse='')
  h <- as.integer(regmatches(svg,regexec('height="([0-9]+)"',svg))[[1]][2])
  b$Emulation$setDeviceMetricsOverride(width=1200,height=h,deviceScaleFactor=2,mobile=FALSE)
  b$Emulation$setDefaultBackgroundColorOverride(color=list(r=0,g=0,b=0,a=0))
  b$Page$navigate(paste0('file:///',gsub(' ','%20',file.path(d,paste0(n,'.html')),fixed=TRUE)))
  b$Runtime$evaluate('document.fonts.ready',awaitPromise=TRUE)
  png <- b$Page$captureScreenshot(format='png',captureBeyondViewport=FALSE)$data
  writeBin(base64enc::base64decode(png),file.path(d,paste0(n,'.png')))
  cat(n,'PNG transparente actualizado.\n')
 }
},finally=b$close())
