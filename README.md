## nrf52_qtc_proj

Creates Qt Creator basic project from any NRF52 SDK's Makefile.

```
    python3 projify.py /home/nRF5_SDK_15.3.0_59ac345/examples/peripheral/blinky/pca10040/blank/armgcc/Makefile
```

Project files ```%proj_name%.creator```, ```%proj_name%.config```, ```%proj_name%.includes``` and ```%proj_name%.files``` will be saved in Makefile directory.

Tested with ```nRF5_SDK_15.3.0_59ac345```.