echo "huraaaaaaaaaaaa"

rc-service cupsd restart

rc-service cupsd status

openrc

touch /run/openrc/softlevel

rc-service cupsd status

rc-service cupsd restart

rc-service cupsd status

# lpadmin -p TM- -v socket://192.168.192.168/TM- -P tm-impact-receipt-rastertotmir.ppd -E
