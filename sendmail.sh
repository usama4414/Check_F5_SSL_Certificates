#TO="musama@i2cinc.com"
TO="itops.cm@i2cinc.com"
From="cm.automation@i2cinc.com"
SUBJ="[F5 SSL Certificates Info][SV5][WDC]"
CC=""
BODY="Please find the attached reports, having SSL Certificates info of F5, both SV5 and WDC."
(
cat << !
From : ${From}
To : ${TO}
Subject : ${SUBJ}
Cc : ${CC}
${BODY}
!

uuencode /u/Projects/F5_SSL_Certificates_Info/check_f5_ssl_certificates/report_199.96.216.197.html "Path to report: /u/Projects/F5_SSL_Certificates_Info/check_f5_ssl_certificates/report_199.96.216.197.html" && uuencode /u/Projects/F5_SSL_Certificates_Info/check_f5_ssl_certificates/report_199.96.219.197.html "Path to report: /u/Projects/F5_SSL_Certificates_Info/check_f5_ssl_certificates/report_199.96.219.197.html"

) | /usr/sbin/sendmail -f ${From} -v ${TO}
