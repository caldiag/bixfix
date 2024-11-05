import sys
from routines import probe
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog='bixfix', description='Verificar e corrigir erros comuns do agente Zabbix em servidores Rihappy.')
  parser.add_argument('user')
  parser.add_argument('password')
  parser.add_argument('-p', '--passive', # roda rotina de sondagem e gera logs, porém não efetua reinstalações ou ajustes.
                    action='store_true')
  parser.add_argument('-l', '--light-fix', # só atualiza arquivos de configuração
                    action='store_true')
  parser.add_argument('-f', '--force-fix') # deve ser parametrizada com um range de lojas (ex. 0,20), e força a reinstalação
  args = parser.parse_args()

  with open("stores.txt", 'r') as file:
    lines = file.readlines()
    stores = [line.strip() for line in lines]

  probe.start(stores, args)