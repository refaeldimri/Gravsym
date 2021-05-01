FROM python:3.8

RUN apt update && \
apt -y upgrade && \
apt install python3-pip apache2 nano libgl1-mesa-glx -y && \
a2dismod mpm_event && \
a2enmod mpm_prefork cgi && \
sed -i "1 a <Directory /var/www/html>" /etc/apache2/sites-enabled/000-default.conf && \
sed -i "2 a Options +ExecCGI" /etc/apache2/sites-enabled/000-default.conf && \
sed -i "3 a DirectoryIndex index.py" /etc/apache2/sites-enabled/000-default.conf && \
sed -i "4 a </Directory>" /etc/apache2/sites-enabled/000-default.conf && \
sed -i "5 a AddHandler cgi-script .py" /etc/apache2/sites-enabled/000-default.conf && \
chmod -R 755 /var/www/html && \
pip3 install mysql-connector-python && \
pip3 install tensorflow && \
pip3 install keras && \
pip3 install opencv-python && \
pip3 install imageai --upgrade && \
pip3 install numpy

EXPOSE 80
VOLUME /var/www/html
CMD chmod -R 755 /var/www/html && service apache2 start && bash
