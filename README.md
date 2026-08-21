# local-demands-api

## Ideia do projeto:
Consiste em uma API que registra demandas de determinada localização.
As demandas podem ser desde problemas estruturais ate simples tarefas corriqueiras que acontecem nas localidades.
As demandas são registradas por endereço, que geralmente contam com dados detalhados como Rua, Bairro, Cidade e Estado.

## Como rodar a API:
*   Baixe o projeto
*   Recomendado criar um ambiente virtual:
```
python3 -m venv venv
```

(linux)
```
source ./venv/bin/activate
```
(windows)
```
./venv/scripts/activate
```
*   Com o ambiente virtual ativado, instale as dependencias:
```
pip install -r requirements.txt
```
*   Após a instalação, execute o comando:
```
python app.py
```


## Regras de negocio:
### Moradores
*  [x] Todo morador pode postar uma demanda
*  [x] Apenas o gerenciador (sindico) pode finalizar uma demanda
*  [ ] Só pode haver 1 associação por rua 
*  [ ] Qualquer morador pode criar ou participar de uma associação
*  [ ] O morador que criar a associaçao, automaticamente vira o sindico
*  [ ] O sindico não pode ser trocado
*  [ ] Somente o sindico pode deletar a associação

### Demanda
* [x] Quando criada, tem que ter um morador e um endereço
* [x] Quando criada, possui status inicial de PENDENTE
* [x] Uma vez marcada como FINALIZADA, não pode ser mais alterada

### Endereços
* [x] O registro de endereços é sempre publico
