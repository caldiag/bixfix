from fabric import Connection

def start(stores, args):
  for store in stores:
    try:
      print(f"\033[94mAJUSTANDO {store}\033[0m")
      conn = Connection(
          host=f"10.{store[:2] + '.' + store[2:]}.1",
          user=args.user,
          connect_kwargs={"password": args.password},
          connect_timeout=2
      )
      conn.config.sudo.password = args.password

      res = []

      def install():
        download = conn.sudo("wget https://repo.zabbix.com/zabbix/7.0/ubuntu/pool/main/z/zabbix-release/zabbix-release_latest+ubuntu16.04_all.deb -O zabbix.deb --no-check-certificate", hide=True)
        print(download.stdout + download.stderr)
        unpack = conn.sudo("dpkg -i zabbix.deb", hide=True)
        print(unpack.stdout + unpack.stderr)

        try:
          # um erro aqui pode não ser fatal. apenas printar.
          update = conn.sudo("apt update", hide=True)
          print(update.stdout + update.stderr)
        except Exception as e:
          print(e)
        
        install = conn.sudo("yes N | apt install -y zabbix-agent", hide=True) #TODO isso está falhando pois novas versões do zabbix tentam mudar o arquivo conf, o que abre um prompt de confirmação do APT
        print(install.stdout + install.stderr)

      if not args.light_fix: install()

      systemctl = conn.sudo("systemctl enable zabbix-agent", hide=True)
      print(systemctl.stdout + systemctl.stderr)

      try:
        # um erro aqui pode não ser fatal. apenas printar.
        dir1 = conn.sudo(r"mkdir -p /etc/zabbix/zabbix_agentd.d", hide=True)
        dir2 = conn.sudo(r"mkdir -p /var/log/zabbix", hide=True)
        res.append(dir1.stdout + dir1.stderr + dir2.stdout + dir2.stderr)
      except Exception as e:
        print(e)
      
      permissions = conn.sudo(r"setfacl -m u:zabbix:rwx /var/log/zabbix", hide=True)
      configs = conn.sudo(r"sed -i '/^ServerActive=/c\ServerActive=172.16.0.49,172.26.0.176' /etc/zabbix/zabbix_agentd.conf", hide=True)
      service = conn.sudo(r"systemctl restart zabbix-agent.service", hide=True)
      res.append(permissions.stdout + permissions.stderr + configs.stdout + configs.stderr + service.stdout + service.stderr) #concatenar output dos comandos anteriores

      with open(f"logs/fix_logs/success/{store}.txt", 'w') as file:
        file.write("\n".join(res))

    except Exception as e:
        with open(f"logs/fix_logs/error/{store}.txt", 'w') as file:
          file.write(str(e))
        print(e)