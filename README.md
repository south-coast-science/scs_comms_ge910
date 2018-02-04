# scs_comms_ge910
Communications abstractions for the South Coast Science Telit GE910 cellular modem board.

_Contains command line utilities and library classes._


**Required libraries:** 

* Third party: Adafruit_BBIO
* SCS root: scs_core
* SCS host: scs_host_bbe or scs_host_bbe_southern


**Branches:**

The stable branch of this repository is master. For deployment purposes, use:

    git clone --branch=master https://github.com/south-coast-science/scs_comms_ge910.git


**Example PYTHONPATH:**

BeagleBone, in /root/.bashrc:

    export PYTHONPATH=/home/debian/SCS/scs_dev/src:/home/debian/SCS/scs_osio/src:/home/debian/SCS/scs_mfr/src:/home/debian/SCS/scs_psu/src:/home/debian/SCS/scs_comms_ge910/src:/home/debian/SCS/scs_dfe_eng/src:/home/debian/SCS/scs_host_bbe/src:/home/debian/SCS/scs_core/src:$PYTHONPATH
