# Instalação do projeto

Crie um ambiente virtual para instalação dos requirements.

## Front-end

Estamos utilizando o padrão do governo federal, por isso precisamos ter instalados o node e o npm, veja a documentação oficial do Node para instalação e execute o seguinte comando dentro da pasta do projeto aonde está o package.json.

```npm
npm install
```

## Back-end

Após instalação do ambiente virtual execute o pip install para instalação de todas as bibliotecas necessárias para o projeto.
```sh
pip install -r requirements.txt
```
Após instalação dos requirements, entre na pasta publicmanager pelo terminal e execute o seguinte comando.
```sh
cp settings_sample.py settings.py
```
Isso irá criar seu arquivo de configurações, faça os ajustes necessários de banco de dados e execute os comandos básicos para iniciar seu projeto.
```py
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

# Padrão de Criação de Branchs

### Correções
- nome_do_dev/fixtures/descricao_breve
### Criação de funcionalidade
- nome_do_dev/feature/descricao_breve
