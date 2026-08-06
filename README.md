# local-demands-api

## Ideia do projeto:
Consiste em uma API que registra problemas locais de uma determinada cidade.
Considere o cenario onde em cidades há em um mesmo bairro, diferentes associaçoes de moradores. Como saber se o mesmo problema pode estar ocorrendo em diferentes ruas. Com essa API, as informações ficam centralizadas facilitando a observação assim como a analise das mesmas.


## Regras de negocio:
### Moradores
*  [x] Todo morador pode postar uma demanda
*  [ ] Apenas o gerenciador (sindico) pode finalizar uma demanda
*  [ ] Só pode haver 1 associação por rua 
*  [ ] Qualquer morador pode criar ou participar de uma associação
*  [ ] O morador que criar a associaçao, automaticamente vira o sindico
*  [ ] O sindico não pode ser trocado
*  [ ] Somente o sindico pode deletar a associação

### Demanda
* [ ] Quando criada, tem que ter um morador e um endereço
* [ ] Quando criada, possui status inicial de PENDENTE
* [ ] Uma vez marcada como FINALIZADA, não pode ser mais alterada

### Endereços
* [ ] O registro de endereços é sempre publico
