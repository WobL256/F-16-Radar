# F-16CM Block 50 Radar Simulation

This is a simple python program that uses PyGame
to render an accurate F-16CM Block 50 radar MFD
page. It is not 100% complete (yet).

![20230213_005821](https://user-images.githubusercontent.com/54248805/218342468-1ef02bdc-9f95-4b99-8e3f-5874579127d1.jpg)

Above is a screenshot of the simulated radar
display on February 13. It's look may or may not
have changed since then (but should mostly look
the same).

There are currently no targets/enemies to lock on,
but they are planned. Also planned is an OpenGL
implementation to integrate a 3D representation
of the radar coverage in front of the aircraft.
This will come after a serious restructuring of
the simulator.

Currently only the right side buttons (range,
azimuth, elevation settings) are functional.
The top row of buttons functionality is planned.
This will include ACM radar functionality,
switching radar modes from CRM to ACM,
Track-While-Scan (TWS) mode, Expand modes
(basically zoom function), Radar Override and
the Control menu.

*GM, GMT and SEA modes may be implemented too.

It supports both mobile and desktop. If it is
running on mobile,the MOBILE_MODE variable in
**radar.py** must be set to True.
