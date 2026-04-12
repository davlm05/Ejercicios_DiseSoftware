#!/bin/bash
cd "$(dirname "$0")/../guides-service"
echo "Starting guides-service on port 8082 (dev)..."
./gradlew run
