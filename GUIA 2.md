# GUIA 2: Revisar y recuperar versiones de Git

Esta guía explica cómo revisar todo el historial, identificar una versión concreta, inspeccionarla sin modificar el proyecto, recuperar archivos o devolver el contenido del repositorio a una versión anterior, volver a subir esa recuperación a GitHub y realizar estas operaciones directamente desde GitHub cuando eres el creador o tienes permisos de escritura.

## 1. Qué significa una versión en Git

En Git, una versión normalmente corresponde a un **commit**. Cada commit tiene:

- Un identificador, por ejemplo `b1b5837`.
- Un autor.
- Una fecha.
- Un mensaje.
- El conjunto de cambios guardados en ese momento.

Una fusión también crea un commit de merge. Por eso el número de commits no siempre equivale al número de cambios funcionales.

Antes de recuperar una versión, conserva una copia de cualquier cambio local no guardado.

## 2. Comprobar el estado actual

Entra en la carpeta del repositorio y ejecuta:

```bash
cd RUTA_DEL_REPOSITORIO
git status --short --branch
```

La primera línea muestra la rama actual. Las líneas que empiezan por `M` indican archivos modificados. Las líneas que empiezan por `??` indican archivos nuevos sin seguimiento.

Guarda cambios locales temporalmente antes de cambiar de versión:

```bash
git stash push -m "Cambios locales antes de revisar versiones"
```

`git stash` guarda temporalmente cambios no confirmados dentro del repositorio local. No los sube a GitHub.

Comprueba los guardados temporales:

```bash
git stash list
```

## 3. Actualizar el historial desde GitHub

Antes de consultar versiones remotas, descarga la información más reciente:

```bash
git fetch --all --prune
```

- `git fetch` descarga commits y referencias sin modificar tus archivos actuales.
- `--all` consulta todos los remotos.
- `--prune` elimina referencias locales de ramas remotas que ya no existen.

Comprueba los remotos:

```bash
git remote -v
```

Comprueba las ramas:

```bash
git branch -a
```

## 4. Revisar todas las versiones

Muestra el historial completo de todas las ramas y remotos:

```bash
git log --all --oneline --graph --decorate
```

Ejemplo de lectura:

```text
* eb58da5 Merge pull request #2
* b1b5837 Simulacion de senales de ruido
* 5c9ac3d Commit inicial
```

El identificador corto de cada línea permite seleccionar esa versión.

Cuenta los commits únicos accesibles desde las referencias locales:

```bash
git rev-list --all --count
```

Lista solo los identificadores completos:

```bash
git log --all --format="%H" --reverse
```

Muestra la historia de una rama concreta:

```bash
git log main --oneline --decorate --graph
```

Muestra el historial de un archivo:

```bash
git log --all --oneline -- config.py
```

Muestra qué cambió en cada commit:

```bash
git show --stat ID_DEL_COMMIT
git show ID_DEL_COMMIT
```

`--stat` muestra un resumen de archivos y líneas. Sin `--stat`, `git show` muestra el diff completo.

## 5. Comparar versiones antes de recuperar

Compara dos commits:

```bash
git diff ID_VERSION_ANTERIOR ID_VERSION_NUEVA
```

Compara `main` con un commit antiguo:

```bash
git diff main ID_DEL_COMMIT
```

Comprueba qué archivos existían en una versión:

```bash
git ls-tree -r --name-only ID_DEL_COMMIT
```

Comprueba el contenido de un archivo en una versión antigua sin cambiar tu archivo actual:

```bash
git show ID_DEL_COMMIT:config.py
```

## 6. Revisar temporalmente una versión

Para abrir el proyecto en una versión concreta sin mover ninguna rama:

```bash
git switch --detach ID_DEL_COMMIT
```

Este estado se llama `detached HEAD`. Permite examinar, ejecutar y probar los archivos de ese commit, pero los commits creados allí no pertenecen automáticamente a una rama.

Comprueba que estás en la versión correcta:

```bash
git status
git log -1 --oneline
```

Para volver a la rama principal:

```bash
git switch main
```

Si tenías cambios guardados con `stash`, recupéralos después:

```bash
git stash list
git stash pop
```

`git stash pop` aplica el guardado y lo elimina de la lista. Para aplicarlo sin eliminarlo, usa:

```bash
git stash apply stash@{0}
```

## 7. Recuperar solo un archivo antiguo

Si solo necesitas restaurar `config.py` desde una versión concreta:

```bash
git restore --source=ID_DEL_COMMIT -- config.py
```

Revisa el resultado:

```bash
git diff -- config.py
```

Si quieres conservarlo, crea una nueva versión en la rama actual:

```bash
git add config.py
git commit -m "Recupera config.py desde una version anterior"
```

Este procedimiento no cambia todo el repositorio; solo reemplaza el archivo indicado.

## 8. Restaurar todo el contenido a una versión anterior de forma segura

La forma recomendada para un repositorio compartido es crear una rama de recuperación. Primero vuelve a `main` y actualízala:

```bash
git switch main
git pull origin main
```

Crea la rama:

```bash
git switch -c restaurar-version
```

Restaura todos los archivos al estado de un commit antiguo:

```bash
git restore --source=ID_DEL_COMMIT --staged --worktree .
```

- `--source` indica la versión de origen.
- `--staged` actualiza el área de preparación.
- `--worktree` actualiza los archivos del directorio de trabajo.
- `.` significa todos los archivos del directorio actual.

Revisa cuidadosamente qué se va a cambiar:

```bash
git status
git diff --cached
git diff
```

Si existen archivos creados después del commit que no aparecen como eliminados, elimínalos manualmente solo después de verificar que pertenecen a la versión posterior. Para eliminar un archivo rastreado:

```bash
git rm nombre-del-archivo
```

Guarda la recuperación como un nuevo commit:

```bash
git commit -m "Restaura el contenido a una version anterior"
```

Este método no borra el historial. Añade un commit nuevo que deja el contenido actual igual que la versión elegida.

## 9. Volver a subir la recuperación a GitHub

Envía la rama de recuperación:

```bash
git push -u origin restaurar-version
```

En GitHub:

1. Abre el repositorio.
2. Pulsa **Compare & pull request**.
3. Selecciona `restaurar-version` como origen.
4. Selecciona `main` como destino.
5. Describe qué versión se está recuperando y por qué.
6. Revisa la lista de archivos eliminados o restaurados.
7. Solicita una revisión.
8. Pulsa **Create pull request**.
9. Después de aprobarlo, pulsa **Merge pull request** y **Confirm merge**.

Actualiza la copia local después de fusionar:

```bash
git switch main
git pull origin main
```

La recuperación ya estará publicada en `main`, pero los commits posteriores seguirán visibles en el historial.

## 10. Revertir una fusión sin reescribir el historial

Si lo que quieres es deshacer una fusión completa, identifica el commit de merge:

```bash
git log main --oneline --merges
```

Crea una rama para el revert:

```bash
git switch main
git pull origin main
git switch -c revertir-fusion
```

Revierte el merge indicando que el primer padre es la línea principal:

```bash
git revert -m 1 ID_DEL_COMMIT_DE_MERGE
```

Si aparecen conflictos:

```bash
git status
```

Edita los archivos con conflicto, elimina las marcas de conflicto, y después:

```bash
git add archivo-resuelto.py
git revert --continue
```

Si decides cancelar el revert:

```bash
git revert --abort
```

Sube la rama y crea un Pull Request:

```bash
git push -u origin revertir-fusion
```

Este método es preferible a `git reset --hard` en `main` compartido porque conserva el historial público y permite revisión.

## 11. Recuperar una versión directamente desde GitHub

Si eres el creador del repositorio o tienes permisos de escritura, puedes iniciar el proceso desde GitHub.

### Opción A: revisar un commit

1. Abre el repositorio en GitHub.
2. Pulsa **Code**.
3. Pulsa el enlace de historial, normalmente **Commits**.
4. Busca el commit que quieres revisar.
5. Pulsa el identificador o el mensaje del commit.
6. Revisa los archivos y el diff.
7. Pulsa **Browse files** para ver el proyecto completo en ese punto histórico.

Esta opción solo revisa la versión; no cambia `main`.

### Opción B: crear una rama desde un commit antiguo

1. Abre el historial de commits.
2. Abre el commit elegido.
3. Pulsa **Browse files**.
4. Usa el selector de ramas o la opción para crear una rama desde ese commit, cuando esté disponible.
5. Pon un nombre como `restaurar-version`.
6. Crea la rama.

Si la interfaz no ofrece crear la rama desde esa página, puedes hacerlo localmente con:

```bash
git fetch origin
git switch -c restaurar-version ID_DEL_COMMIT
git push -u origin restaurar-version
```

### Opción C: revertir un Pull Request fusionado

Para deshacer los cambios de un Pull Request concreto:

1. Abre la pestaña **Pull requests**.
2. Selecciona **Closed**.
3. Abre el Pull Request fusionado.
4. Busca el botón **Revert**.
5. Pulsa **Revert**.
6. GitHub creará una rama y un nuevo Pull Request.
7. Revisa los cambios propuestos.
8. Fusiona el nuevo Pull Request cuando esté aprobado.

El botón **Revert** no borra la fusión original; crea cambios nuevos que la deshacen.

Si no aparece **Revert**, puede ser porque no tienes permisos suficientes, porque la fusión tiene conflictos o porque el método de fusión no permite una reversión automática. En ese caso, realiza el revert localmente y crea el Pull Request manualmente.

## 12. Restaurar `main` directamente: advertencia

No muevas `main` hacia atrás con `git reset --hard` y `git push --force` en un repositorio compartido salvo que el equipo lo haya acordado expresamente. Ese procedimiento reescribe la historia y puede eliminar referencias a commits posteriores.

El método recomendado es:

1. Identificar la versión.
2. Revisarla.
3. Crear una rama de recuperación.
4. Restaurar el contenido.
5. Crear un nuevo commit.
6. Subir la rama.
7. Abrir un Pull Request.
8. Revisar y fusionar.

## 13. Lista final de comprobación

Antes de recuperar una versión:

```bash
git status
git fetch --all --prune
git log --all --oneline --graph --decorate
```

Antes de subir una recuperación:

```bash
git status
git diff --cached
git log -1 --oneline
```

Después de fusionar en GitHub:

```bash
git switch main
git pull origin main
git status
```

El último `git status` debería indicar que tu rama local está sincronizada y sin cambios pendientes.
