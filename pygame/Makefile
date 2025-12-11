SHELL := cmd.exe

run:
	@echo EXECUTANDO ...
	call venv\Scripts\activate.bat && python Sussurros_da_Selva\jogo.py

enviroments:
	@echo CRIANDO AMBIENTE ...
	python -m venv venv

build: enviroments
	@echo INSTALANDO DEPENDENCIAS ...
	call venv\Scripts\activate.bat && pip install -r requirements.txt
