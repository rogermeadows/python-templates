from plumbum import SshMachine

remote = SshMachine('intrepid', user='ubuntu', keyfile='/home/rmeadows/.ssh/id_rsa')
r_ls = remote['ls']
print 'intrepid: /opt/repos/github:'
with remote.cwd('/opt/repos/github'):
    print r_ls()

