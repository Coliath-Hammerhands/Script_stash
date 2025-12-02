# Option 1: Full access for owner (you), but no access for other accounts.

chmod 700 /home/MYUSERNAME/Videos/private

This setting can be undone from your account without password by typing

chmod 775 /home/MYUSERNAME/Videos/private

# Option 2: No access for any user including you, so you need to become root to enter the directory.

chmod 000 /home/MYUSERNAME/Videos/private

This can also be reverted from your account without password by

chmod 775 /home/MYUSERNAME/Videos/private

# Option 3: No access for any user including you and no chance to revert it from your account, so every action can only be performed as root.

chmod 700 /home/MYUSERNAME/Videos/private

sudo chown root: /home/MYUSERNAME/Videos/private

To revert this setting, you have to do the following (which needs sudo and therefore requires your account password):

sudo chown MYUSERNAME: /home/MYUSERNAME/Videos/private

chmod 775 /home/MYUSERNAME/Videos/private