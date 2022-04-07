#!/bin/sh

NOW="$(date)"

alembic revision --autogenerate -m "$NOW"