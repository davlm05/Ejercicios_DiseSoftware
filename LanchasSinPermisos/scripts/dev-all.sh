#!/bin/bash
SCRIPT_DIR="$(dirname "$0")"

echo "=== Lanchas Sin Permisos - Dev Mode ==="
echo "Starting all services..."

bash "$SCRIPT_DIR/dev-tours.sh" &
TOURS_PID=$!

bash "$SCRIPT_DIR/dev-guides.sh" &
GUIDES_PID=$!

sleep 10

bash "$SCRIPT_DIR/dev-frontend.sh" &
FRONTEND_PID=$!

echo ""
echo "All services started:"
echo "  - Tours:    http://localhost:8081/tours"
echo "  - Guides:   http://localhost:8082/guides"
echo "  - Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services"

trap "kill $TOURS_PID $GUIDES_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
