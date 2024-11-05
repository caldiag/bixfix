# bixfix

bixfix é um utilitário de terminal desenvolvido para verificar, corrigir e refazer instalações do agente zabbix em servidores.

## Instalação:
```
git clone https://github.com/caldiag/bixfix
cd bixfix
python3 main.py
```
## Parâmetros
`--passive (-p)`: apenas realiza a verificação do status Zabbix em servidores, pulando a etapa de instalação ou ajuste. Gera logs hierárquicos no diretório atual.<br/>
`--light-fix (-l)`: ajusta os arquivos de configurações, pastas e diretórios do servidor, e reinicia o serviço Zabbix. NÃO reinstala o Zabbix. (recomendado)<br/>
`--force-fix (-f)`: recebe um range de lojas como parâmetro (ex: 0,20) para serem ajustadas, independente dos resultados da verificação de status, ou se o servidor já está configurado corretamente ou não. (recomendado juntamente com `--light-fix`)<br/>

## Exemplos de uso
`python3 main.py`: faz a sondagem total de todos os servidores, coletando qualquer um com serviço Zabbix inoperante e os parametrizando na função de AJUSTE. O Zabbix de todos servidores problemáticos será reinstalado e ajustado (não recomendado, demorado)</br>
`python3 main.py --force-fix 0,20 --light-fix`: configura e reinicia (mas não reinstala) os serviços do Zabbix nos servidores das lojas do range especificado. (1002-1025 nesse caso)</br>
`python3 main.py --passive`: faz a sondagem total de todos os servidores, porém não realiza qualquer instalação ou ajustes. Os logs ainda serão salvos, fornecendo informações úteis sobre o status Zabbix em todos os servidores.</br>
