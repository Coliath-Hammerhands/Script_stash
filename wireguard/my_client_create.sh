#! /usr/bin/env bash
client_name="$1"
client_number="$2"

bash ./client_create.sh "10.100.0." "fd08:4711::" "api.coletime.fun:47111" $client_number $client_name
