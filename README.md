# Welcome to my exciting Drone project!

The primary objective of this project is to develop a program that enables real-time display of the drone's location as it soars through the sky.


```
                                                     _,--=--._
                                                   ,'    _    `.
                                                  -    _(_)_o   -
                                             ____'    /_  _/]    `____
                                      -=====::(+):::::::::::::::::(+)::=====-
                                               (+).""""""""""""",(+)
                                                   .           ,
                                                     `  -=-  '               
```

## Project status & Roadmap:

**Work in Progress:** This project is currently under active development. <br>
Thank you for your interest and patience as I continue to work on the project.

## Technical aspects:

A GPS module is placed on an MKR1000, which is attached to the drone. <br>

The C++ program is continuously receiving the #GNGGA sequences from the GPS module and writes the GPS data to the server. 
<br><br>
Additionally, a Python program reads the data sent from the Arduino via Telnet, extracts the latitude, longitude and altitude values and displays them in the web browser using a Django server.

## Why this project?

Here are a few real-world scenarios where drone control becomes a significant asset:<br>

- **Precision agriculture:** surveying large fields, monitoring crop health and gathering data on soil conditions. <br>
- **Photography and videography:** providing unique perspectives and accessing challenging locations.<br>
- **Surveillance and security:** monitoring large areas and tracking movement in real-time.<br>
- **Search and rescue operations:** locating missing persons in difficult terrains. <br>
- **Environement monitoring:** collecting data on deforestation, wildlife populations and air quality.<br>
- **Delivery services:** transporting medical supplies or essential items in areas with limited access terrains.<br>
