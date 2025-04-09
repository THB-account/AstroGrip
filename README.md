# AstroGrip
glove_driver is the script/frame work to develop the application from. This should be runnable on any pc without any additional sensors required.
The last training_release is used for the actual glove.

A project from the student initiative Bears at Technical University Berlin. This repo documents the code is used to control the AstroGrip glove based measurement system.

A general class overview for glove_driver/the training release is seen here. On training release only the pressure/temperature sensor and the spectrometer were used.
![ClassDiagram](https://github.com/THB-account/AstroGrip/blob/main/doc/ClassDiagram.svg)
The general structure is layer based, for which there are the model, buffer, sensor and data layer. Interaction between the main loop and data aswell as sensors happens trough the Buffer classes.

![FlowChart](https://github.com/THB-account/AstroGrip/blob/main/doc/FlussDiagramm.svg)

