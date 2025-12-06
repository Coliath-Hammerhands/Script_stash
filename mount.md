# for uuid
```bash
lsblk -f
```

# after backup 

```bash
sudo nano /etc/fstab
```

add line

UUID=<UUID of your external device> /mnt/<your mount point>       <file system Ex: ext4>    noatime,x-systemd.automount,x-systemd.device-timeout=10,x-systemd.idle-timeout=1min 0 2

# mine

UUID=6e18b026-2589-45d0-aae7-cf233966e638 /mnt/4tbhdd ext4 noatime,x-systemd.automount,x-systemd.device-timeout=10,x-systemd.idle-timeout=1min 0 2