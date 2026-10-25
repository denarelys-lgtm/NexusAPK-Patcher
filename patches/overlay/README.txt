
Los archivos del parche van aquí.
Reproduce las rutas que aparecen dentro del APK descompilado.
Ejemplos:
AndroidManifest.xml
res/values/strings.xml
smali/com/ejemplo/app/MainActivity.smali

No añadas archivos de ejemplo que puedan sobrescribir archivos reales.


# NexusAPK Patcher

Sistema para descargar un APK desde GitHub Releases, descompilarlo,
aplicar archivos de parche, reconstruirlo y firmarlo mediante GitHub Actions.

## Requisitos

- Repositorio público o privado con Actions habilitado.
- APK original alojado en una GitHub Release accesible sin autenticación.
- Enlace directo del archivo APK.
- Archivos de parche en patches/overlay/.

## Ejecutar

1. Abre la pestaña Actions.
2. Selecciona NexusAPK Patcher.
3. Pulsa Run workflow.
4. En release_url, pega el enlace directo del APK.
5. En patch_name, escribe el nombre del parche.
6. Ejecuta el workflow.
7. Abre la ejecución y descarga el artefacto NexusAPK-<nombre>.

## Crear parches

Coloca los archivos modificados dentro de patches/overlay/.
La estructura debe coincidir con las rutas del proyecto descompilado
por Apktool.

Para eliminar archivos, añade sus rutas relativas a patches/delete.txt,
una por línea.

## Limitaciones importantes

- La firma creada es temporal y cambia en cada ejecución.
- No se puede instalar como actualización de una aplicación firmada
  con otro certificado.
- No se garantiza que todos los APK se reconstruyan correctamente.
- Los APK con bibliotecas nativas, protecciones especiales o formatos
  no compatibles pueden necesitar pasos adicionales.
- El proceso no modifica automáticamente el código Java decompilado
  por JADX: los cambios de código se aplican mediante Smali u otros
  archivos que Apktool pueda reconstruir.
- La verificación de firma no equivale a una prueba funcional.
