gcc -fPIC -DDBG -c -I. -o secexec.o secexec.c
gcc -shared -Wl,-soname,libsecexec.so.1  -o libsecexec.so.1.0.1 secexec.o -lc
sudo chown root:root libsecexec.so.1.0.1
sudo chmod u+s libsecexec.so.1.0.1
ln -s libsecexec.so.1.0.1 libsecexec.so.1
ln -s libsecexec.so.1 libsecexec.so
