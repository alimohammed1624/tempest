#!/bin/sh
gunicorn -b '0.0.0.0:8002' src.app:app