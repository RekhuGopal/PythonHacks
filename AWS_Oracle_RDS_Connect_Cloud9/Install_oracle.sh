sudo su -

cd /etc/yum.repos.d
wget http://yum.oracle.com/public-yum-ol7.repo
wget http://yum.oracle.com/RPM-GPG-KEY-oracle-ol7
rpm --import RPM-GPG-KEY-oracle-ol7
yum install -y yum-utils
yum-config-manager --enable ol7_oracle_instantclient
yum install -y oracle-instantclient18.3-sqlplus

exit

echo "export ORACLE_HOME=/usr/lib/oracle/18.3/client64/" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=/usr/lib/oracle/18.3/client64/lib/" >> ~/.bashrc
echo "export PATH=$PATH:/usr/lib/oracle/18.3/client64/bin" >> ~/.bashrc
. ~/.bashrc

