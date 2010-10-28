gcc -DDBG -DGETOPT -DJAIL -I. -o secexec secexec.c
sudo chown root:root secexec
sudo chmod u+s secexec
