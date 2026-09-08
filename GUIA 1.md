# GUIA 1: Git y GitHub desde cero

Esta guía explica paso a paso cómo configurar Git, conectar un repositorio local con GitHub mediante HTTPS y un Personal Access Token (PAT), trabajar con forks, copiar repositorios, modificar archivos, guardar versiones, subir cambios y crear un Pull Request.

## 1. Conceptos básicos

- **Git**: programa que guarda el historial de cambios de un proyecto.
- **Repositorio local**: copia del proyecto que está en tu computadora.
- **Repositorio remoto**: copia del proyecto alojada en GitHub.
- **Commit**: una versión guardada localmente con un mensaje.
- **Rama**: una línea de trabajo independiente.
- **`main`**: rama principal que normalmente debe mantenerse estable.
- **Pull Request**: solicitud para revisar y fusionar cambios de una rama en otra.
- **PAT**: token que GitHub utiliza como credencial al trabajar mediante HTTPS.

## 2. Instalar y verificar Git

Instala Git desde <https://git-scm.com/downloads> si todavía no está instalado.

Verifica la instalación:

```bash
git --version
```

Este comando muestra la versión de Git instalada. Si aparece un número como `git version 2.x.x`, Git está disponible.

## 3. Configurar la cuenta de Git

Configura el nombre que aparecerá en tus commits:

```bash
git config --global user.name "Tu Nombre"
```

Configura el correo asociado con tu cuenta de GitHub:

```bash
git config --global user.email "tu-correo@example.com"
```

Establece `main` como nombre predeterminado para nuevos repositorios:

```bash
git config --global init.defaultBranch main
```

Revisa la configuración:

```bash
git config --global --list
```

La opción `--global` aplica la configuración a todos los repositorios de tu usuario en ese equipo.

## 4. Crear un fork en GitHub

Un fork es una copia de un repositorio de otra persona dentro de tu propia cuenta de GitHub. Es útil cuando no tienes permiso para modificar directamente el repositorio original.

1. Inicia sesión en GitHub.
2. Abre el repositorio original.
3. Pulsa **Fork**.
4. Selecciona tu cuenta como propietario.
5. Mantén el nombre del repositorio o cambia el nombre si es necesario.
6. Pulsa **Create fork**.

Después tendrás dos repositorios:

- **Upstream**: repositorio original.
- **Origin**: tu fork, donde tienes permiso para subir ramas.

## 5. Copiar un repositorio de GitHub al equipo

En GitHub, abre tu fork y pulsa **Code**. Copia la URL HTTPS. Tendrá una forma parecida a esta:

```text
https://github.com/TU_USUARIO/REPOSITORIO.git
```

Clona el repositorio:

```bash
git clone https://github.com/TU_USUARIO/REPOSITORIO.git
```

`git clone` descarga los archivos, el historial y la configuración de conexión remota.

Entra en la carpeta creada:

```bash
cd REPOSITORIO
```

Comprueba el repositorio remoto:

```bash
git remote -v
```

Normalmente verás `origin` apuntando a tu fork.

Si necesitas añadir el repositorio original como `upstream`:

```bash
git remote add upstream https://github.com/USUARIO_ORIGINAL/REPOSITORIO.git
```

Comprueba ambos remotos:

```bash
git remote -v
```

Puedes copiar un directorio en PowerShell con:

```powershell
Copy-Item .\REPOSITORIO .\COPIA_REPOSITORIO -Recurse
```

También puedes crear una carpeta:

```powershell
New-Item -ItemType Directory -Path datos
```

En Git Bash o Linux, las equivalencias son:

```bash
cp -r REPOSITORIO COPIA_REPOSITORIO
mkdir datos
```

## 6. Verificar el estado y las versiones

Comprueba el estado del repositorio:

```bash
git status
```

Este comando indica la rama actual y si hay archivos modificados, preparados o sin seguimiento.

Muestra la rama actual:

```bash
git branch --show-current
```

Muestra todas las ramas locales:

```bash
git branch
```

Muestra las ramas locales y remotas:

```bash
git branch -a
```

Muestra el historial resumido:

```bash
git log --oneline --graph --decorate --all
```

Cada línea representa un commit o una versión guardada. La parte inicial, como `a1b2c3d`, es el identificador corto del commit.

Cuenta los commits accesibles desde todas las referencias locales:

```bash
git rev-list --all --count
```

Descarga información nueva de GitHub sin cambiar tus archivos:

```bash
git fetch origin
```

## 7. Crear una rama de trabajo

Actualiza primero `main`:

```bash
git switch main
git pull origin main
```

`git switch main` cambia a la rama principal. `git pull origin main` descarga y combina los cambios recientes de GitHub.

Crea una rama para tu tarea:

```bash
git switch -c mi-cambio
```

La opción `-c` crea la rama y cambia a ella inmediatamente.

Confirma que estás en la rama correcta:

```bash
git branch --show-current
```

Conviene crear una rama por tarea, por ejemplo `corrige-documentacion` o `agrega-pruebas`. Así `main` permanece estable.

## 8. Modificar archivos

Edita los archivos desde VS Code. Por ejemplo, modifica `config.py` o `README.md`.

Después revisa qué cambió:

```bash
git status
git diff
```

`git diff` muestra diferencias que todavía no se han preparado para un commit.

Para revisar un archivo concreto:

```bash
git diff -- config.py
```

## 9. Preparar y guardar cambios

Prepara un archivo específico:

```bash
git add config.py
```

Prepara varios archivos:

```bash
git add config.py README.md
```

Prepara todos los cambios del directorio actual:

```bash
git add .
```

Antes de crear el commit, revisa exactamente lo preparado:

```bash
git diff --cached
```

Guarda los cambios como una nueva versión:

```bash
git commit -m "Agrega simulacion de senales de ruido"
```

`git commit` crea una versión local. El mensaje debe explicar qué cambio se realizó.

Comprueba el último commit:

```bash
git log -1 --oneline
git status
```

## 10. Conectar por HTTPS y autenticar con PAT

El remoto HTTPS tiene un formato similar a este:

```text
https://github.com/TU_USUARIO/REPOSITORIO.git
```

Si el remoto es incorrecto, cámbialo:

```bash
git remote set-url origin https://github.com/TU_USUARIO/REPOSITORIO.git
```

Para crear un PAT en GitHub:

1. Abre GitHub y entra en **Settings**.
2. Entra en **Developer settings**.
3. Selecciona **Personal access tokens**.
4. Elige **Fine-grained tokens**.
5. Selecciona el repositorio que vas a modificar.
6. Concede `Contents: Read and write`.
7. Genera el token y cópialo de forma segura.

GitHub muestra el token una sola vez. Cuando Git solicite credenciales:

```text
Username: TU_USUARIO
Password: pega_aqui_el_PAT
```

El PAT se escribe en el campo de contraseña aunque no sea una contraseña normal. La terminal no muestra caracteres al pegarlo; eso es normal.

Nunca publiques el PAT, lo guardes en un archivo del proyecto o lo incluyas en una URL. Si se expone, revócalo en GitHub y crea otro.

## 11. Subir la rama a GitHub

La primera vez que subas `mi-cambio`:

```bash
git push -u origin mi-cambio
```

- `git push` envía commits al remoto.
- `origin` es el nombre del remoto.
- `mi-cambio` es la rama que se envía.
- `-u` conecta la rama local con su rama remota correspondiente.

En los siguientes envíos puedes usar:

```bash
git push
```

Verifica en GitHub que aparezca la rama. Si aparece un error `403`, comprueba que el PAT pertenece a la cuenta correcta, que tiene permiso de escritura sobre el repositorio y que el remoto apunta a tu fork.

## 12. Crear el Pull Request

Después de subir la rama:

1. Abre tu repositorio en GitHub.
2. Cambia el selector de ramas a `mi-cambio`.
3. Pulsa **Compare & pull request**.
4. Selecciona `main` como rama de destino.
5. Escribe un título claro.
6. Explica qué modificaste.
7. Indica cómo verificaste el cambio.
8. Solicita revisores.
9. Pulsa **Create pull request**.

Un Pull Request no es todavía una fusión. Es una propuesta para que otras personas revisen tus commits antes de incorporarlos a `main`.

## 13. Responder a una revisión

Si un revisor solicita cambios, permanece en la misma rama, modifica los archivos y ejecuta:

```bash
git status
git diff
git add archivo-modificado.py
git commit -m "Corrige observaciones de la revision"
git push
```

El Pull Request se actualiza automáticamente con el nuevo commit.

## 14. Fusionar y actualizar el repositorio local

Cuando la revisión esté aprobada:

1. Abre el Pull Request.
2. Comprueba los archivos modificados.
3. Verifica que las comprobaciones pasen.
4. Pulsa **Merge pull request**.
5. Pulsa **Confirm merge**.

Después actualiza tu repositorio local:

```bash
git switch main
git pull origin main
```

Para borrar una rama ya fusionada:

```bash
git branch -d mi-cambio
git push origin --delete mi-cambio
```

Borrar la rama no borra los commits que ya forman parte del historial de `main`.

## 15. Flujo resumido

```bash
git switch main
git pull origin main
git switch -c nueva-tarea

# Editar archivos

git status
git diff
git add .
git commit -m "Describe el cambio"
git push -u origin nueva-tarea
```

Después crea el Pull Request, espera la revisión, atiende los comentarios, fusiona en GitHub y actualiza `main` localmente.
