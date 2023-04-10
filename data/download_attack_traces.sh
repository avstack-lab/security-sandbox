#!/usr/bin/env bash

set -e

SAVEDIR=${1:-./attack_traces/}

LINK="https://g-b0ef78.1d0d8d.03c0.data.globus.org/security/cyber-attack/traces.zip"

mkdir -p $SAVEDIR
wget $LINK
unzip "traces.zip" -d $SAVEDIR
rm "traces.zip"
