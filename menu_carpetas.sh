#!/usr/bin/env bash
# ---------------------------------------------------------------------
# TRABAJO PRÁCTICO - Gestión de carpetas vía menú
# Alumno: Gauna Nahuel
# Descripción: Crea un workspace en /tmp/tp_carpetas_$USER y opera SOLO allí.
# Requisitos: bash, mkdir, ls, mv, rmdir, rm, read, find, sed, sort
# ---------------------------------------------------------------------

set -o errexit
set -o pipefail
set -o nounset

# --- Preparación del workspace ---
USER_NAME="${USER:-usuario}"
WORKSPACE="/tmp/tp_carpetas_${USER_NAME}"
mkdir -p "$WORKSPACE"
cd "$WORKSPACE"

# --- Utilidades ---
# trim: recorta espacios al inicio/fin
trim() {
  # usa sed para recortar espacios en blanco
  echo -e "$1" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//'
}

# valida que un nombre de carpeta sea aceptable
validar_nombre() {
  local raw="$1"
  local name
  name="$(trim "$raw")"

  # prohibir vacío, rutas absolutas, /, y secuencias ".."
  if [[ -z "$name" ]]; then
    echo "Error: el nombre no puede estar vacío." >&2
    return 1
  fi
  if [[ "$name" = /* ]]; then
    echo "Error: no se permiten rutas absolutas." >&2
    return 1
  fi
  if [[ "$name" == *"/"* ]]; then
    echo "Error: no se permite el carácter '/' en el nombre." >&2
    return 1
  fi
  if [[ "$name" == "." || "$name" == ".." || "$name" == *".."* ]]; then
    echo "Error: no se permite usar '.' o '..'." >&2
    return 1
  fi
  # seguridad adicional: evitar nombres vacíos tras trim
  if [[ -z "$name" ]]; then
    echo "Error: el nombre no puede quedar vacío tras recortar espacios." >&2
    return 1
  fi

  # imprimir el nombre saneado al stdout (para capturarlo)
  echo "$name"
  return 0
}

pausa() {
  read -rp $'Presioná ENTER para continuar… ' _tmp
}

listar_carpetas() {
  # muestra solo directorios a nivel 1 dentro del workspace
  # opción con find para evitar dependencias de globbing
  find . -maxdepth 1 -mindepth 1 -type d -printf '%f\n' | sort
}

crear_carpeta() {
  read -rp "Nombre de la carpeta a crear: " entrada
  if ! nombre=$(validar_nombre "$entrada"); then
    pausa; return
  fi

  if [[ -d "$nombre" ]]; then
    echo "Aviso: la carpeta '$nombre' ya existe. No se crea."
  else
    mkdir "$nombre"
    echo "OK: carpeta '$nombre' creada en $WORKSPACE."
  fi
  pausa
}

renombrar_carpeta() {
  read -rp "Nombre de carpeta ORIGEN: " origen_in
  if ! origen=$(validar_nombre "$origen_in"); then
    pausa; return
  fi
  read -rp "Nuevo nombre DESTINO: " destino_in
  if ! destino=$(validar_nombre "$destino_in"); then
    pausa; return
  fi

  if [[ ! -d "$origen" ]]; then
    echo "Error: no existe la carpeta origen '$origen'."
    pausa; return
  fi
  if [[ -e "$destino" ]]; then
    echo "Error: ya existe un archivo o carpeta con el nombre destino '$destino'."
    pausa; return
  fi

  mv -- "$origen" "$destino"
  echo "OK: '$origen' fue renombrada a '$destino'."
  pausa
}

eliminar_carpeta() {
  read -rp "Nombre de la carpeta a eliminar: " entrada
  if ! nombre=$(validar_nombre "$entrada"); then
    pausa; return
  fi

  if [[ ! -d "$nombre" ]]; then
    echo "Error: no existe la carpeta '$nombre'."
    pausa; return
  fi

  # intentar borrar solo si está vacía
  if rmdir -- "$nombre" 2>/dev/null; then
    echo "OK: carpeta '$nombre' eliminada (estaba vacía)."
  else
    echo "Aviso: la carpeta '$nombre' no está vacía."
    read -rp "¿Querés forzar el borrado recursivo? (S/N): " resp
    case "${resp^^}" in
      S|SI|SÍ)
        rm -rf -- "$nombre"
        echo "OK: carpeta '$nombre' eliminada de forma recursiva."
        ;;
      *)
        echo "Operación cancelada. No se eliminó la carpeta."
        ;;
    esac
  fi
  pausa
}

mostrar_menu() {
  clear
  cat <<EOF
==============================================
   MENÚ - Gestión de carpetas (Workspace)
   Workspace: $WORKSPACE
==============================================
1) Crear carpeta
2) Listar carpetas
3) Renombrar carpeta
4) Eliminar carpeta
5) SALIR
EOF
}

# --- Bucle principal ---
while true; do
  mostrar_menu
  read -rp "Elegí una opción [1-5]: " op
  case "$op" in
    1) crear_carpeta ;;
    2)
       echo "Carpetas en '$WORKSPACE':"
       listado="$(listar_carpetas || true)"
       if [[ -z "$listado" ]]; then
         echo "(no hay carpetas)"
       else
         printf '%s\n' "$listado"
       fi
       pausa
       ;;
    3) renombrar_carpeta ;;
    4) eliminar_carpeta ;;
    5)
       echo "Saliendo. El workspace queda disponible en: $WORKSPACE"
       exit 0
       ;;
    *)
       echo "Opción inválida. Elegí entre 1 y 5."
       pausa
       ;;
  esac
done
