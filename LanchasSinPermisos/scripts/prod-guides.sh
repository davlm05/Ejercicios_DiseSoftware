#!/bin/bash
cd "$(dirname "$0")/../guides-service"
echo "Building guides-service..."
./gradlew shadowJar
echo "Running guides-service on port 8082 (prod)..."
java -jar build/libs/guides-*-all.jar
