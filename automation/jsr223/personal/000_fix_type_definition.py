# trying to fix the type definition by executing the following:
# bundle:start-level org.eclipse.smarthome.automation.module.script.rulesupport 90
# bundle:restart org.eclipse.smarthome.automation.module.script.rulesupport
# so:
# first test if the error occurs:
# 
# from org.slf4j import LoggerFactory
# LoggerFactory.getLogger("org.eclipse.smarthome.automation.examples").info("Checking automation bundle status...")

# try:
#     from lucid.rules import rule
# except:
#     LoggerFactory.getLogger("org.eclipse.smarthome.automation.examples").info("Bundle not OK, fixing...")
#     import paramiko

#     ssh = paramiko.SSHClient()
#     ssh.load_system_host_keys()
#     #-p 8101 openhab@localhost
#     ssh.connect('localhost', port=8081 ,username='openhab', password='habopen')
#     # check start level

#     # if start level != 90
#     ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('bundle:start-level org.eclipse.smarthome.automation.module.script.rulesupport 90')

#     # restart bundle
#     ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('bundle:restart org.eclipse.smarthome.automation.module.script.rulesupport')

#     ssh.close()