#!/usr/bin/env bash

create_upstart() {
  domain=$1
  file=$2
  port=$3
  conf="/etc/init/${domain}_${file}.conf"

  cat > $conf << EOF
#!upstart

description "Node Process - $domain -> $file : $port"
author      "Pieter Michels"

respawn

start on (local-filesystems and net-device-up IFACE=eth0)
stop  on shutdown

script
  export NODE_ENV="production"
  export PORT="$port"
  exec /usr/bin/node /srv/www/$domain/current/$file.js >> /var/www/$domain/shared/logs/$file 2>&1
end script
EOF

  echo $conf

  # Restart upstart script
  stop ${domain}_${file}
  start ${domain}_${file}

  echo Restarted ${domain}_${file}
}

create_upstart "$1" "$2" "$3"
