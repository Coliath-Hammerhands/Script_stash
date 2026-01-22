sudo apt update && sudo apt install samba

sudo nano /etc/samba/smb.conf

# in file

[4tbhdd]
comment = 4tbhdd mount
path = /mnt/4tbhdd
browsable = yes
writable = yes
guest ok = no
read only = no
create mask = 0775
directory mask = 0775
valid users = cole
[20Thdd]
comment = 20 Terrabyte mount
path = /mnt/20Thdd
browsable = yes
writable = yes
guest ok = no
read only = no
create mask = 0777
directory mask = 0777
valid users = cole

# cont

sudo smbpasswd -a yourusername
sudo systemctl restart smbd
