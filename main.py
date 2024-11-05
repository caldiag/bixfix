import sys
from routines import probe
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog='bixfix', description='Verificar e corrigir erros comuns do agente Zabbix em servidores Rihappy.')
  parser.add_argument('user')
  parser.add_argument('password')
  parser.add_argument('-p', '--passive',
                    action='store_true')
  parser.add_argument('-f', '--force-fix')
  args = parser.parse_args()

  with open("stores.txt", 'r') as file:
    lines = file.readlines()
    stores = [line.strip() for line in lines]

  probe.start(stores, args.user, args.password, args.passive, args.force_fix)