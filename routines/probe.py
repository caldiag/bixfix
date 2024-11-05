import sys
from fabric import Connection
from utils.directory import ensure_directory_exists
import socket
from invoke.exceptions import UnexpectedExit
import paramiko
from . import patch

# esta função realiza uma série de validações em um servidor, algumas das quais irão levantar erros. ela os captura e gera logs
# conforme necessário, além de coletar servidores falhados para parametrizar a função de patch.

def start(stores, args):
  ensure_directory_exists('success')
  ensure_directory_exists('no_zabbix')
  ensure_directory_exists('no_auth')
  ensure_directory_exists('misc_error')
  ensure_directory_exists('fix_logs/success')
  ensure_directory_exists('fix_logs/error')

  if args.passive and args.force_fix:
    print("--force-fix e --passive são mutuamente exclusivos.")
    return

  if args.force_fix:
    start, end = map(int, args.force_fix.split(','))
    patch.start(stores[start:end+1], args)
    return
  
  no_zabbix_stores = []

  for store in stores:
      success_file = f'logs/success/{store}.txt'
      no_zabbix_file = f'logs/no_zabbix/{store}.txt'
      misc_error_file = f'logs/misc_error/{store}.txt'
      no_auth_file = f'logs/no_auth/{store}.txt'

      print(f"\033[94mSONDANDO {store}\033[0m")
      try:
        conn = Connection(host=f"10.{store[:2] + '.' + store[2:]}.1", user=user, connect_kwargs={"password": password}, connect_timeout=2)

        zabbix_result = conn.run('systemctl status zabbix-agent', hide=True)

        if "Loaded: loaded" in zabbix_result.stdout:
          with open(success_file, 'w') as file:
            file.write(zabbix_result.stdout)
          continue

        if zabbix_result.stderr:
          no_zabbix_stores.append(store)
          with open(misc_error_file, 'w') as file:
            file.write(zabbix_result.stderr)
          continue

        # qualquer retorno além de sucesso ou stderr (deve ser tratado manualmente, como erros de sudo, erros de hostname, etc.)
        with open(misc_error_file, 'w') as file:
          file.write(zabbix_result.stdout)

      except UnexpectedExit as e:
        # quando zabbix não está instalado, o systemctl retorna código de erro 3,
        # que é levantado como exception UnexpectedExit pelo Fabric
        if("No such file or directory" in str(e)):
          no_zabbix_stores.append(store)
          with open(no_zabbix_file, 'w') as file:
            file.write(str(e))
          return
        with open(misc_error_file, 'w') as file:
          file.write(str(e))

      except paramiko.ssh_exception.AuthenticationException as e:
        with open(no_auth_file, 'w') as file:
          file.write(f"Failed to authenticate (incorrect password?): {e}")

      except socket.gaierror as e:
        with open(misc_error_file, 'w') as file:
          file.write(f"Network error (gaierror): {e}")

      # caso de fallback
      except Exception as e:
        print(e)
        with open(misc_error_file, 'w') as file:
          file.write(f"Error: {e}")

  if not passive:
    patch.start(no_zabbix_stores, args)
    return