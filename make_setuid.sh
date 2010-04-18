#! /bin/bash
rm -f codechecker/backend/setuid_helper
make codechecker/backend/setuid_helper
cd codechecker/backend
sudo chown root:root setuid_helper && sudo chmod u+s setuid_helper
cd ../../
