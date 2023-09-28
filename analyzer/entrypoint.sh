#!/bin/sh
gunicorn -b '0.0.0.0:8001' src.app:app