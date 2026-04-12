#!/bin/bash
cd "$(dirname "$0")/../tours-service"
echo "Starting tours-service on port 8081 (dev)..."
./gradlew run
