## https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/configuring-the-self-hosted-runner-application-as-a-service

# use root by running 
sudo su -
cd <path of folder actions-runner from confuration>

# Installing 
./svc.sh install

# Ensure runsvc.sh is Executable
chmod +x /home/testvmuser/actions-runner/runsvc.sh

# Check File Ownership
chown testvmuser:testvmuser /home/testvmuser/actions-runner/runsvc.sh

# Verify SELinux Status

sestatus

# If enabled run below
setenforce 0

# then restart the service it should work
systemctl restart actions.runner.RekhuGopal-CloudCostOptimize.rhelvmgithubrunner.service


