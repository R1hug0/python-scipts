#!/bin/bash

jname() {
#根据你的环境修改name的获取方式，获取你本机的java进程名
name=($(ps -ef | grep -v grep |grep tomcat | awk '{print $9}'| awk -F"/" '{print $5}'))
printf '{\n'
printf '\t"data":[\n'
  for key in ${!name[@]}
    do 
      if [[ "${#name[@]}" -gt 1 && "${key}" -ne "$((${#name[@]}-1))" ]];then
        printf '\t {\n'
        printf "\t\t\t\"{#PROCESSNAME}\":\"${name[${key}]}\"},\n"
      else [[ "${key}" -eq "$((${#name[@]}-1))" ]]
        printf '\t {\n'
        printf "\t\t\t\"{#PROCESSNAME}\":\"${name[${key}]}\"}\n"
      fi
    done
printf '\t ]\n'
printf '}\n'
}
jname
