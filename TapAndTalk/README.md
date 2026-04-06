This is the technical documentation for my ergonomic dictophone prototype named Tap and Talk.

The main.cpp file is the code that is running on the ESP32. It assigns capacative touch pins to the five copper pad buttons on the device, 
and creates booleans that are false so that the device knows not to send signals too early. Each time the loop runs, it checks all five pads 
to see if they were pressed; if so, it sends the corresponding message via serial connection. For each pad, it checks if it has already been
touched so it doesn't send continuous messages if you hold down the pad. There is also a small delay to help debounce.

The index.html file displays the UI for Tap and Talk, and updates displaying what status and mode the program is in. It also contains CSS
styling I used to make the display aesthetic but simple, and the javascript code that it needed in order to interact with the app.py file.
Handling the renaming so the user could change the names of recordings was the hardest part; it required lots of fiddling with the refreshing,
so that the page wouldn't reload the recordings while the user was trying to rename it. The playback functionality was also difficult for
this reason, but I just tweaked the refreshFromServer() function to not refresh the recordings or playback while the user was actively 
renaming or listening to a recording. Rendering the recordings just required some formatting, which I used ChatGPT to help me with.

Lastly, the app.py file runs the flask app that is used for the UI. It is a large file with a lot of routes, but the most important ones
are the ones for each of the buttons. There is a "/toggle_record" route that is used when the user presses the record/stop button, and 
corresponding routes for the rest of them, which call helper methods to execute the user's requests. The file handles the starting and 
stopping of recording, storage, downloading, playing, etc(everything except displaying the UI and detecting when the user presses the pads).
It also sets up a serial listener with the serial_listener() function, so that it constantly listens for messages on the ESP32 and can
carry out the user's requests.

The actual device required lots of trial and error to set up. At first my wires were way too long and my pads were way too small, so that 
when connected to the device, their values did not change much at all when touched(for example, they would rest at 89 and drop to 88 
consistently when touched, but a difference of 1 is not a stable value to base the device on). So I had to remake the pads to be much larger,
and the wires to be shorter so that they carried the signal better and also fit within the box without much excess. Once the pads and wires
were the correct size, I taped the ESP32 down inside the box, stuck the pads down, painted the box, and labeled the buttons. The appearance
of the device is very simple, which I think matches what a real dictophone would look like. 

Here are some pictures of the device for reference:
<img width="600" height="800" alt="tapandtalk1 (1)" src="https://github.com/user-attachments/assets/4e9cc82f-f329-4b55-b84a-294ada5cdf92" />
<img width="600" height="800" alt="tapandtalk2 (1)" src="https://github.com/user-attachments/assets/ded4c67a-43b1-47c2-8ffb-cd4ca1ce8eda" />

For more documentation and a demo, click here.
