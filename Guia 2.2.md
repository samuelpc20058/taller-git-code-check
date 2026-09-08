# Guia 2.2: Corregir errores y recuperar versiones por HTTPS

Guia corta para revisar el historial, corregir cambios y recuperar versiones desde la terminal integrada de VS Code usando HTTPS con GitHub.

## 1. Comprobar el estado antes de tocar nada

En la terminal de VS Code entra en el proyecto:

```bash
cd RUTA_DEL_REPOSITORIO
git status --short --branch
```

Guarda temporalmente cambios locales que aun no quieras confirmar:

```bash
git stash push -m "Cambios antes de revisar versiones"
```

Comprueba los guardados:

```bash
git stash list
```

## 2. Descargar el historial mas reciente

```bash
git fetch --all --prune
```

Este comando actualiza las referencias locales sin modificar tus archivos actuales.

Comprueba ramas y versiones:

```bash
git branch -a
git log --all --oneline --graph --decorate
```

El identificador corto, como `b1b5837`, identifica una version concreta.

Contar las versiones guardadas como commits:

```bash
git rev-list --all --count
```

## 3. Revisar una version antes de recuperarla

Ver el contenido y los cambios de un commit:

```bash
git show ID_DEL_COMMIT
```

Ver solo el resumen:

```bash
git show --stat ID_DEL_COMMIT
```

Comparar dos versiones:

```bash
git diff ID_VERSION_ANTERIOR ID_VERSION_NUEVA
```

Ver un archivo antiguo sin cambiar el actual:

```bash
git show ID_DEL_COMMIT:config.py
```

## 4. Probar una version sin cambiar ninguna rama

Cambia temporalmente a la version elegida:

```bash
git switch --detach ID_DEL_COMMIT
```

Ahora puedes abrir los archivos y probarlos. Este estado se llama `detached HEAD` y es normal para una revision temporal.

Vuelve a la rama principal al terminar:

```bash
git switch main
```

Recupera los cambios guardados temporalmente:

```bash
git stash pop
```

## 5. Recuperar solo un archivo

Desde la rama donde quieres aplicar la recuperacion:

```bash
git switch main
git pull origin main
git restore --source=ID_DEL_COMMIT -- config.py
```

Revisa el resultado:

```bash
git diff -- config.py
```

Guarda la recuperacion:

```bash
git add config.py
git commit -m "Recupera config.py desde una version anterior"
```

## 6. Recuperar todo el proyecto de forma segura

Crea una rama para que la recuperacion pueda revisarse:

```bash
git switch main
git pull origin main
git switch -c recuperar-version
```

Restaura todos los archivos al commit elegido:

```bash
git restore --source=ID_DEL_COMMIT --staged --worktree .
```

Revisa que archivos cambiaran:

```bash
git status
git diff --cached
```

Si hay archivos rastreados creados despues de esa version y ya no deben existir:

```bash
git rm nombre-del-archivo
```

Crea el commit de recuperacion:

```bash
git commit -m "Restaura el proyecto a una version anterior"
```

## 7. Subir la recuperacion a GitHub

```bash
git push -u origin recuperar-version
```

Si Git solicita credenciales HTTPS, usa tu usuario y el PAT como contraseña. No compartas el PAT.

En GitHub:

1. Abre el repositorio.
2. Pulsa **Compare & pull request**.
3. Selecciona `recuperar-version` como origen y `main` como destino.
4. Revisa las eliminaciones y restauraciones.
5. Crea el Pull Request.
6. Aprueba y fusiona con **Merge pull request**.

Actualiza el repositorio local:

```bash
git switch main
git pull origin main
git status
```

La recuperacion queda registrada como un commit nuevo; el historial anterior no se borra.

## 8. Deshacer una fusion o un commit compartido

Para localizar fusiones:

```bash
git log main --oneline --merges
```

Crea una rama para deshacer una fusion:

```bash
git switch main
git pull origin main
git switch -c revertir-fusion
git revert -m 1 ID_DEL_COMMIT_DE_MERGE
```

Sube la rama:

```bash
git push -u origin revertir-fusion
```

Crea un Pull Request hacia `main` y fusiona despues de revisarlo.

Para deshacer un commit normal:

```bash
git revert ID_DEL_COMMIT
git push
```

`git revert` crea un commit nuevo que deshace cambios sin borrar el historial.

## 9. Corregir conflictos

Si Git informa de conflictos:

```bash
git status
```

Abre en VS Code los archivos marcados, conserva el contenido correcto y elimina las marcas `<<<<<<<`, `=======` y `>>>>>>>`.

Despues:

```bash
git add archivo-resuelto.py
git revert --continue
```

Si quieres cancelar la operacion:

```bash
git revert --abort
```

Para un conflicto durante un merge usa:

```bash
git merge --abort
```

## 10. Recuperar desde GitHub como creador del repositorio

Para revisar sin cambiar nada:

1. Abre el repositorio en GitHub.
2. Pulsa **Commits**.
3. Abre el commit deseado.
4. Pulsa **Browse files**.
5. Revisa los archivos de esa version.

Para deshacer un Pull Request fusionado:

1. Abre **Pull requests**.
2. Selecciona **Closed**.
3. Abre el Pull Request fusionado.
4. Pulsa **Revert**.
5. Revisa el Pull Request nuevo que GitHub crea.
6. Fusiona el nuevo Pull Request.

**Revert** no elimina el Pull Request original: crea un cambio nuevo que deshace sus modificaciones.

Si no aparece **Revert**, usa la recuperacion local de esta guia, sube una rama y crea el Pull Request manualmente.

## 11. Volver al estado actual

Despues de revisar cualquier version:

```bash
git switch main
git pull origin main
```

Si habias usado `stash`:

```bash
git stash pop
```

Antes de terminar:

```bash
git status
git log -1 --oneline
```

No uses `git reset --hard` ni `git push --force` en `main` compartido: pueden reescribir el historial y ocultar cambios de otros colaboradores.
