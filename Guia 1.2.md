# Guia 1.2: Tomar, modificar y subir un repositorio por HTTPS

Guia corta para trabajar desde la terminal integrada de VS Code con un repositorio de GitHub usando HTTPS y un PAT.

## 1. Abrir la terminal de VS Code

En VS Code abre **Terminal > New Terminal**. Comprueba que estas en la carpeta correcta:

```powershell
Get-Location
```

Lista los archivos:

```powershell
Get-ChildItem
```

## 2. Obtener el repositorio

En GitHub abre el repositorio o tu fork, pulsa **Code > HTTPS** y copia la URL. Despues ejecuta:

```bash
git clone https://github.com/USUARIO/REPOSITORIO.git
cd REPOSITORIO
```

`git clone` descarga el proyecto y su historial completo.

Verifica la conexion:

```bash
git remote -v
git status
```

El remoto normalmente se llama `origin`.

## 3. Configurar la cuenta de Git

Hazlo una sola vez en el equipo:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@example.com"
```

Comprueba la configuracion:

```bash
git config --global --list
git --version
```

## 4. Preparar una rama de trabajo

Actualiza `main`:

```bash
git switch main
git pull origin main
```

Crea una rama nueva:

```bash
git switch -c mi-cambio
```

Confirma la rama activa:

```bash
git branch --show-current
```

## 5. Modificar archivos desde VS Code

Edita los archivos en el explorador de VS Code. Despues revisa los cambios:

```bash
git status
git diff
```

Para copiar un archivo o directorio en PowerShell:

```powershell
Copy-Item .\archivo.py .\respaldo.py
Copy-Item .\datos .\respaldo -Recurse
```

## 6. Guardar los cambios como una version

Prepara archivos concretos:

```bash
git add archivo.py README.md
```

O prepara todos los cambios:

```bash
git add .
```

Revisa lo preparado:

```bash
git diff --cached
```

Crea el commit:

```bash
git commit -m "Describe el cambio realizado"
```

Verifica la version creada:

```bash
git log -1 --oneline
git status
```

## 7. Configurar autenticacion HTTPS con PAT

En GitHub crea un token desde **Settings > Developer settings > Personal access tokens**. Selecciona el repositorio y concede `Contents: Read and write`.

No pegues el token en comandos ni archivos. Cuando Git lo solicite durante el `push`, escribe:

```text
Username: TU_USUARIO
Password: pega_el_PAT_aqui
```

La terminal no mostrara caracteres al escribir el PAT. Es normal.

## 8. Subir la rama a GitHub

La primera vez:

```bash
git push -u origin mi-cambio
```

- `origin`: repositorio remoto.
- `mi-cambio`: rama local que se envia.
- `-u`: enlaza la rama local con la remota.

Las siguientes veces:

```bash
git push
```

Si aparece un error `403`, comprueba que el PAT tenga escritura, que pertenezca a la cuenta correcta y que `git remote -v` apunte a tu repositorio o fork.

## 9. Crear y completar el Pull Request

En GitHub:

1. Abre el repositorio.
2. Selecciona la rama `mi-cambio`.
3. Pulsa **Compare & pull request**.
4. Selecciona `main` como destino.
5. Explica el cambio y las comprobaciones realizadas.
6. Pulsa **Create pull request**.
7. Espera la revision y atiende los comentarios.

Para corregir una observacion, vuelve a editar en VS Code y ejecuta:

```bash
git add .
git commit -m "Corrige observaciones del Pull Request"
git push
```

El Pull Request se actualiza automaticamente.

## 10. Fusionar y actualizar el equipo local

Cuando el Pull Request este aprobado, en GitHub pulsa **Merge pull request** y **Confirm merge**.

Despues, en la terminal:

```bash
git switch main
git pull origin main
```

Para comprobar que todo quedo sincronizado:

```bash
git status
```
