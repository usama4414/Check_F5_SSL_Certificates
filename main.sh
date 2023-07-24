set -x
docker run -v /u/Projects/F5_SSL_Certificates_Info/check_f5_ssl_certificates:/app   --name f5_cert_generator f5_ssl_cert_info --f5.ip=199.96.216.197 --f5.user=certmon --f5.password=Sys101/china1 -w45 -c15
if [[ "$?" != 0 ]]
then 
    echo "Docker run Failed, Please Check"
    /u/Projects/F5_SSL_Certificates_Info/check_f5_ssl_certificates/sendmail_err.sh "199.96.216.197"
else
    docker rm f5_cert_generator
    docker run -v /u/Projects/F5_SSL_Certificates_Info/check_f5_ssl_certificates:/app   --name f5_cert_generator f5_ssl_cert_info --f5.ip=199.96.219.197 --f5.user=certmon --f5.password=Sys101/china1 -w45 -c15
    if [[ "$?" != 0 ]]
    then
    	echo "Docker run Failed, Please Check"
    	/u/Projects/F5_SSL_Certificates_Info/check_f5_ssl_certificates/sendmail_err.sh "199.96.219.197"
    else
	docker rm f5_cert_generator
    	/u/Projects/F5_SSL_Certificates_Info/check_f5_ssl_certificates/sendmail.sh
    fi
fi 
