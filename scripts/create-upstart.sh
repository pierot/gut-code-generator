#!/usr/bin/env bash

create_upstart() {
  domain=$1
  project=$2
  file=$3
  port=$4

  #####################################

  path="/srv/www/$domain/public/$project/$file.js"
  path_logs="/srv/logs/$domain"
  upstart=${domain}_${project}_${file}

  #####################################

  conf="/etc/init/$upstart.conf"

  #####################################

  echo "Create log path $path_logs"

  mkdir -p $path_logs

  #####################################

  echo "Installed app at $path"

  cat > $conf << EOF
#!upstart

description "Node Process - $domain -> $path : $port"
author      "Pieter Michels"

respawn

start on (local-filesystems and net-device-up IFACE=eth0)
stop  on shutdown

script
  export NODE_ENV="production"
  export PORT="$port"

  exec /usr/bin/node $path >> $path_logs/$file.log 2>&1
end script
EOF

  #####################################

  # Restart upstart script
  stop ${upstart}
  start ${upstart}

  #####################################

  echo "Restarted $upstart"
}

create_upstart "$1" "$2" "$3" "$4"
