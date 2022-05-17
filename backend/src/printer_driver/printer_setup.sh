openrc

touch /run/openrc/softlevel

rc-service cupsd start

rc-update add cupsd boot

rc-service cupsd restart

# lpadmin -p TM- -v socket://192.168.192.168/TM- -P tm-impact-receipt-rastertotmir.ppd -E

