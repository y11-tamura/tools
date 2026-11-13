#!/bin/bash


IP=$(hostname -i)
HOSTNAME=$(hostname)
case $HOSTNAME in
    vslm* | pdgx* )
        echo "/share/app/schrodinger/SCHRODINGER_2026-3"
        ;;
    ECLS* )
        echo "/home/app/schrodinger/SCHRODINGER_2026-3"
        ;;
    * )
        case $IP in
            10.82.* )
                echo "/home/app/schrodinger/SCHRODINGER_2026-3"
                ;;
            * )
                echo "Unknown hostname"
                exit
                ;;
        esac
esac


