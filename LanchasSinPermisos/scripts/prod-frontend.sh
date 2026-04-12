#!/bin/bash
cd "$(dirname "$0")/../frontend"
echo "Building frontend..."
npm run build
echo "Serving frontend on port 4173 (preview)..."
npm run preview
