# Raven Backup

Raven Backup es una aplicación de escritorio en Python 3.10 con interfaz gráfica Tkinter para realizar copias de seguridad locales y remotas usando `rsync`. Permite programar tareas con `cron`, comprimir durante la copia, copia incremental, y gestionar enlaces simbólicos.
Ha sido desarrolada sobre el sistema operativo GNU/Linux, utilizando sus características
y usando comandos del sistema a través de subprocesos.

---

## 🚀 Características

- Copias de seguridad locales y remotas (SSH)
- Soporte para copia incremental
- Opción de comprimir durante la copia
- Eliminar archivos en destino si se borran en origen 
- Gestión de enlaces simbólicos: mantener o copiar archivos
- Programador de tareas con `cron`
- Interfaz multilingüe (Español / Inglés)
- Almacenamiento seguro de contraseñas con cifrado AES (Fernet)
- Registro de logs y estado en tiempo real

---

## 🛠️ Requisitos
- Python 3.10+
- Módulo `venv`para Python
- `tkinter` 
- `Git` (para clonar el repositorio)
- `cryptography` (encripta la password)
- `babel` (para compilación de traducciones)
- `rsync` 
---

## 📦 Instalación

1. La forma más fácil es descargar del repositorio el script [`install_raven.sh`](https://github.com/DDorfm/raven_backup/blob/main/install/install_raven.sh).
Este script clonará el repositorio, creará un entorno virtual y un script
lanzador de la aplicación. Puedes ejecutarlo desde el directorio de descargas.
No olvides aplicarle permisos de ejecución (chmod +x)


2. Si quieres hacerlo manualmente...

- Clona el repositorio:
   ```bash
   git clone https://github.com/DDorfm/raven_backup.git
   cd raven-backup
 	```
- Crea un entorno de ejecución dentro del directorio raven_backup

	```bash
	python3- m venv venv
	```

- Instala dependencias

	```bash
	pip install -r reqeriments.txt
	```

-  Ejecuta la app
	```bash
	python3 raven_backup.py
	```
>Nota: git clone descargará todo el contenido del repositorio incluído el script de instalación automática install_raven.sh situado en el directorio install/ . Si elige la opción manual de instalación puede eliminar este directorio y su contenido.
---

## ⚙️ Configuración inicial
1. Selecciona archivos/directorios de origen con los botones Elegir ficheros o Elegir directorios.

2. Define el destino (local o remoto: usuario@host:ruta).

3. Configura opciones:
	```bash
	- Eliminar en destino si se borra en origen

	- Comprimir durante la copia
	
	- Copia incremental

	- Tratamiento de enlaces simbólicos
	```

4. Para acceso remoto:
	```bash

	- Elige tipo de acceso: contraseña o clave pública

	- Indica puerto SSH y contraseña (si aplica)
	```
> Nota: raven_backup crea un fichero de configuración oculto llamado `.raven_backup.conf`
No edites manuelmente este fichero ni ninguno de los que crea la aplicación
---
## 🌐 Traducciones

La aplicación compila al iniciarse el fichero de idiomas. Por tanto
no se necesita una compilación manual por el usuario. En la versión
actual están disponibles los idiomas Español e Inglés

---

## 🛡️ Seguridad

Las contraseñas se almacenan cifradas con Fernet.
El archivo .secret.key tiene permisos restringidos (chmod 600).
No se almacenan credenciales en texto plano.

---

## ⚖️ Licencia

Raven Backup se proporciona **SIN GARANTÍA ALGUNA**. Es software libre, y puedes redistribuirlo bajo los términos de la Licencia Pública General de GNU.  
Libre para usar, modificar y distribuir — siempre que cualquier versión derivada 
también sea libre.

Derechos y obligaciones según la [**GNU GPL v3.0**](LICENSE).

---

## 🐞 Reportar Bugs

Si encuentras errores, por favor contacta con danieldorfman@proton.me
indicando: 


	- Descripción del problema
	- Paso a paso para reproducirlo
	- Sistema operativo y versión de Python


