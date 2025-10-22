# MLops obesidad documentation!

## Description

Aplicación enfocada en estimar los niveles de obesidad en individuos basándose en sus hábitos alimenticios y condición física.

## Commands

The Makefile contains the central entry points for common tasks related to this project.

### Syncing data to cloud storage

* `make sync_data_up` will use `aws s3 sync` to recursively sync files in `data/` up to `s3://mna-mlops-equipo7-a01795983/data/`.
* `make sync_data_down` will use `aws s3 sync` to recursively sync files from `s3://mna-mlops-equipo7-a01795983/data/` to `data/`.


