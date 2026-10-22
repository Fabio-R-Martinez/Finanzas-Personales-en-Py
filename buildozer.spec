[app]

# (str) Título de la aplicación (el nombre que aparecerá bajo el ícono en Android)
title = Gestor Financiero

# (str) Nombre del paquete (solo letras minúsculas, sin espacios ni caracteres especiales)
package.name = gestorfinanzas

# (str) Dominio del paquete (para identificar de forma única la app en Android)
package.domain = org.finanzas.familiar

# (str) Directorio donde se encuentra el código fuente
source.dir = .

# (list) Extensiones de archivos que Buildozer debe incluir en el APK
# ¡CRÍTICO!: Debes incluir 'kv' para la interfaz gráfica y 'db' para SQLite
source.include_exts = py,png,jpg,kv,db,sql

# (str) Versión de tu aplicación
version = 0.1

# (list) Requisitos de la aplicación
# Librerías de Python necesarias para compilar el paquete nativo
requirements = python3,kivy==2.2.1,kivymd==1.2.0,pillow,sqlite3

# (str) Orientación de la pantalla ('portrait' para vertical, ideal para celulares)
orientation = portrait

# (bool) Indicar si la app ocupa toda la pantalla (1) o conserva la barra de estado (0)
fullscreen = 0

# (str) Ícono de la app (opcional, si tienes una imagen en assets/icon.png)
# icon.filename = %(source.dir)s/assets/icon.png

# (list) Permisos de Android
# Para almacenamiento local en SQLite no se requieren permisos especiales complejos
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (list) Arquitecturas soportadas para celulares modernos
android.archs = arm64-v8a, armeabi-v7a

icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/presplash.png
