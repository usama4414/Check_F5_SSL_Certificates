#TO="musama@i2cinc.com"
TO="itops.cm@i2cinc.com,itops.automation@i2cinc.com"
From="cm.automation@i2cinc.com"
SUBJ="[Error][F5 SSL Certificates Info]"
CC=""
BODY="Some Error occured while fetching Certs Info from F5. The Ip is $1"
(
cat << !
From : ${From}
To : ${TO}
Subject : ${SUBJ}
Cc : ${CC}
${BODY}
!


) | /usr/sbin/sendmail -f ${From} -v ${TO}
