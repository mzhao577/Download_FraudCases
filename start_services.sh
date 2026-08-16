#!/usr/bin/env bash
#
# start_services.sh - start, stop and check the case review web tools.
#
#   ./start_services.sh                      start both, print the links
#   ./start_services.sh status               what is running
#   ./start_services.sh stop                 stop both
#   ./start_services.sh restart              stop, then start
#
#   ./start_services.sh --only webtool2      just one of them
#   ./start_services.sh --csv FILE           point webtool at a summary CSV
#   ./start_services.sh --csv FILE --pdf-dir DIR
#   ./start_services.sh --port 9000 --port2 9001
#   ./start_services.sh --foreground         run one tool in this terminal
#
# webtool  (v1, port 8000) shows the summary; it takes a CSV on the command line.
# webtool2 (v2, port 8001) shows the prevention design under the summary; it
# reads its input folder, so --csv does not apply to it.
#
# Logs go to logs/webtool-<port>.log, one per running instance.
#
# Starting is idempotent: a tool already answering on its port is left alone. To
# load a different CSV into a tool that is already up, use `restart`.

set -uo pipefail

cd -- "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

PYTHON="${PYTHON:-python3}"
PORT1="${PORT1:-8000}"
PORT2="${PORT2:-8001}"
CSV=""
PDF_DIR=""
ONLY=""
FOREGROUND=0
CMD="start"

usage() { awk 'NR<3 {next} /^#/ {sub(/^# ?/, ""); print; next} {exit}' "${BASH_SOURCE[0]}"; exit "${1:-0}"; }
die()   { printf 'error: %s\n' "$*" >&2; exit 1; }

# ------------------------------------------------------------------ arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    start|stop|status|restart) CMD="$1"; shift ;;
    -h|--help)     usage 0 ;;
    --csv)         CSV="${2:?--csv needs a file}"; shift 2 ;;
    --pdf-dir)     PDF_DIR="${2:?--pdf-dir needs a folder}"; shift 2 ;;
    --only)        ONLY="${2:?--only needs webtool or webtool2}"; shift 2 ;;
    --port)        PORT1="${2:?--port needs a number}"; shift 2 ;;
    --port2)       PORT2="${2:?--port2 needs a number}"; shift 2 ;;
    --foreground)  FOREGROUND=1; shift ;;
    *)             die "unknown argument: $1  (try --help)" ;;
  esac
done

[[ -z "$ONLY" || "$ONLY" == "webtool" || "$ONLY" == "webtool2" ]] \
  || die "--only takes webtool or webtool2, not '$ONLY'"

wants() { [[ -z "$ONLY" || "$ONLY" == "$1" ]]; }

# -------------------------------------------------------------------- helpers
pid_of() { pgrep -f "$1/app.py" 2>/dev/null | head -1; }

responds() {  # responds <port>
  [[ "$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "http://127.0.0.1:$1/" 2>/dev/null)" == "200" ]]
}

port_owner() {  # anything at all listening on this port?
  lsof -nP -iTCP:"$1" -sTCP:LISTEN 2>/dev/null | awk 'NR==2 {print $1" (pid "$2")"}'
}

stop_one() {  # stop_one <name> - stops every instance of it, whatever the port
  local pids; pids=$(pgrep -f "$1/app.py" 2>/dev/null | tr '\n' ' ')
  if [[ -n "${pids// /}" ]]; then
    pkill -f "$1/app.py" 2>/dev/null
    sleep 1
    printf '  stopped %-9s (pid %s)\n' "$1" "${pids% }"
  else
    printf '  %-9s was not running\n' "$1"
  fi
}

status_one() {  # status_one <name> <port>
  local pid; pid=$(pid_of "$1")
  if [[ -n "$pid" ]] && responds "$2"; then
    local n; n=$(curl -s --max-time 3 "http://127.0.0.1:$2/api/datasets" \
      | "$PYTHON" -c 'import json, sys
try:
    d = json.load(sys.stdin)[0]
    print("%s, %d cases, %d columns" % (d["key"], d["cases"], len(d["columns"])))
except Exception:
    print("(dataset unknown)")' 2>/dev/null)
    printf '  %-9s RUNNING   http://127.0.0.1:%s   pid %-7s %s\n' "$1" "$2" "$pid" "$n"
  elif [[ -n "$pid" ]]; then
    printf '  %-9s running but not answering on %s (pid %s) - see logs/%s-*.log\n' \
      "$1" "$2" "$pid" "$1"
  else
    printf '  %-9s stopped\n' "$1"
  fi
}

start_one() {  # start_one <name> <port> [extra args...]
  local name="$1" port="$2"; shift 2
  local log="logs/$name-$port.log"   # per port, so a second instance keeps its own

  if responds "$port"; then
    printf '  %-9s already running on %s (pid %s)\n' \
      "$name" "$port" "$(pid_of "$name")"
    [[ -n "$CSV" && "$name" == "webtool" ]] \
      && printf '  %-9s NOTE: --csv ignored - it is already up with its own CSV.\n  %-9s       `restart` to load %s\n' "" "" "$CSV"
    return 0
  fi
  local owner; owner=$(port_owner "$port")
  if [[ -n "$owner" ]]; then
    printf '  %-9s SKIPPED: port %s is taken by %s\n' "$name" "$port" "$owner" >&2
    printf '  %-9s          use --port/--port2 to choose another\n' "" >&2
    return 1
  fi

  mkdir -p logs
  if [[ "$FOREGROUND" -eq 1 ]]; then
    printf '  %-9s foreground on %s (ctrl-c to stop)\n\n' "$name" "$port"
    exec "$PYTHON" -u "$name/app.py" "$@" --port "$port"
  fi

  nohup "$PYTHON" -u "$name/app.py" "$@" --port "$port" --no-browser > "$log" 2>&1 &
  local newpid=$!

  for _ in $(seq 1 30); do          # wait for it to actually answer
    responds "$port" && break
    kill -0 "$newpid" 2>/dev/null || break
    sleep 0.5
  done

  if responds "$port"; then
    # line 2 of the log is the tool's own "<KEY> N cases <- file.csv" line
    printf '  %-9s http://127.0.0.1:%-6s pid %-7s %s\n' \
      "$name" "$port" "$newpid" "$(sed -n '2p' "$log" | sed 's/^ *//')"
  else
    printf '  %-9s FAILED to start - last lines of %s:\n' "$name" "$log" >&2
    tail -5 "$log" | sed 's/^/      /' >&2
    return 1
  fi
}

# ----------------------------------------------------------------- pre-flight
command -v "$PYTHON" >/dev/null || die "'$PYTHON' not found (set PYTHON=/path/to/python3)"
[[ -f webtool/app.py && -f webtool2/app.py ]] \
  || die "run this from the project root (webtool/app.py not found)"

WT1_ARGS=()
if [[ -n "$CSV" ]]; then
  [[ -f "$CSV" ]] || die "CSV not found: $CSV"
  WT1_ARGS+=("$CSV")
  if [[ -n "$PDF_DIR" ]]; then
    [[ -d "$PDF_DIR" ]] || die "PDF folder not found: $PDF_DIR"
    WT1_ARGS+=(--pdf-dir "$PDF_DIR")
  fi
elif [[ -n "$PDF_DIR" ]]; then
  die "--pdf-dir only means something with --csv"
fi
if [[ -n "$CSV" && "$ONLY" == "webtool2" ]]; then
  die "--csv applies to webtool; webtool2 reads its input folder (see --help)"
fi
if [[ -n "$CSV" && -z "$ONLY" ]]; then
  printf 'note: --csv applies to webtool only; webtool2 uses its input folder\n\n'
fi

[[ "$FOREGROUND" -eq 1 && -z "$ONLY" ]] \
  && die "--foreground runs a single tool; add --only webtool or --only webtool2"

# ------------------------------------------------------------------- dispatch
case "$CMD" in
  stop)
    echo "stopping:"
    wants webtool  && stop_one webtool
    wants webtool2 && stop_one webtool2
    ;;
  status)
    echo "services:"
    wants webtool  && status_one webtool  "$PORT1"
    wants webtool2 && status_one webtool2 "$PORT2"
    ;;
  restart|start)
    if [[ "$CMD" == "restart" ]]; then
      echo "stopping:"
      wants webtool  && stop_one webtool
      wants webtool2 && stop_one webtool2
      echo
    fi
    echo "starting:"
    rc=0
    # ${a[@]+"${a[@]}"} keeps an empty array safe under `set -u` on bash 3.2 (macOS).
    wants webtool  && { start_one webtool "$PORT1" ${WT1_ARGS[@]+"${WT1_ARGS[@]}"} || rc=1; }
    wants webtool2 && { start_one webtool2 "$PORT2" || rc=1; }
    echo
    echo "open:"
    wants webtool  && responds "$PORT1" && echo "  webtool   http://127.0.0.1:$PORT1   summary view"
    wants webtool2 && responds "$PORT2" && echo "  webtool2  http://127.0.0.1:$PORT2   prevention design under the summary"
    echo
    echo "stop with: ./start_services.sh stop"
    exit $rc
    ;;
esac
