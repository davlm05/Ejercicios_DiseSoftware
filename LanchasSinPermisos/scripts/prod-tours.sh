#!/bin/bash
cd "$(dirname "$0")/../tours-service"
echo "Building tours-service..."
./gradlew shadowJar
echo "Running tours-service on port 8081 (prod)..."
java -jar build/libs/tours-*-all.jar
