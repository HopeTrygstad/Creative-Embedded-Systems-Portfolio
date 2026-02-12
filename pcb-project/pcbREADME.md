This project began with using Kicad to design the circuit that would power the flashing LED. The schematic was 
provided, and the next step was to use the Kicad PCB editor to place all of the components, and connect all of 
them so that the circuit worked properly. This was a bit tricky, since none of the wires could cross at all as 
they all had to be in one layer. Pins 1-8 of the 555 timer chip had specified components they had to connect to. 
I started by connecting all the resistors to what they had to be connected to, then the LED, then the capacitors,
then the pins of the chip itself. The software also helped me to make sure there were no major violations through the "Run DRC" functionality. Then I saved the gerber files for the outline, drill holes, and edge of the PCB, and converted
them to SVG files using the script provided for the project. 

Once I had the SVG files for the outlines, drill holes and edges, it was time to mill the board. We used a Carvey
CNC to mill. First I used a PCB V-bit to carve the outines, setting a depth of 0.08 mm in order to drill through
the copper of the board, but not all the way through the material underneath. Then I switched the bit to a 1/32 in
drill bit, and lined up the drill holes in Easel to align with the pads of the outline. I added 0.2 mm of depth 
to the cut, to make sure that the holes would go all the way through the board. 

After the machine drilled the holes, I laid the outline of the house over where I had placed the outline, switched
the bit to a 1/8 in double flute straight end mill, and had the machine cut the edge of the PCB. After this was complete, I had a house-shaped PCB with all the wires and hole printed.

The last step was to solder all of the elements to the board. I used all of the same elements as Miles did in the 
tutorial- a 4.7 microfarad capacitor for C1, a 10 nanofarad capacitor for C2, a 4.7 kOhm resistor for R1, a 68 kOhm resistor for R2, and a 100 Ohm resistor for R3. I also used the standard 555 timer chip provided, the battery holder provided, and a small yellow LED. Once I soldered all of the elements to the board and put the battery into the holder, the light began flashing as desired.

To use the device, you just have to slide the battery in with the smooth side facing up. Once it is in, the light will begin to flash! To turn it off, just slide the battery back out.

This folder also includes the SVG files I used for the CNC milling, as well as my final PCB file with the design of my circuit. 

See the creative documentation for this project [here](..project2.md).

Images of the PCB:
![house](https://github.com/user-attachments/assets/7cd85347-d87a-4212-86a3-6610c9686782)
![houseback](https://github.com/user-attachments/assets/e89baa5d-34e0-46b4-9d13-9b1b32cfc71c)


