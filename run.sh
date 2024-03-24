#!/bin/sh

sfda_env() {
    python3 -m venv .venv
}

sfda_reqs() {
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
}

sfda_activate() {
    source .venv/bin/activate
}

sfda_run() {
    python3 main.py
}
