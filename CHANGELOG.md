# Changelog

All notable changes to this project will be documented in this file.

## [1.4.9] - 2026-04-28

### Fixed
- Duplicated window title string in `crea_ventana_root`
- Password overwritten after decryption in `lee_fichero_configuracion`
- `password_var_inicial_str` stored encrypted value instead of plain
- Loose expression `[i]` not indexing correctly in `procesa_datos_origen`
- `break` misindented in `selecciona_ficheros_origen`, loop always
  exited on first iteration
- Inverted logic condition in `cuenta_atras` caused status message
  to always be cleared

### Changed
- Code style: PEP8 compliance via flake8