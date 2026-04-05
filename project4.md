---
layout: default
---

# Ergonomic Dictophone 

This is my submission for the third project in this class: creating a touch sensitive interface with an ESP32, copper tape, wire and my laptop.

My brother is a resident in radiology, and works behind a computer for 10+ hours a day, sometimes 7 days a week, reading scans and talking into a dictophone. He has wrist pain from the constant computer work, even though he uses an ergonomic mouse and keyboard. One thing that could be more ergonomic is the dictophone he uses, since you have to press a button to start recording. Touch sensitive pads in place of buttons would be less stress for the wrists.

My ergonomic dictophone is called "Tap and Talk." It is a painted Dove soap box with five copper pads on it, soddered to wires that connect to the ESP32 inside. The ESP32 sends serial messages via USB to a program on a laptop, which is displayed in a browser and uses Flask to run. There are five buttons: record/stop, resume/continue, delete last, play last, and mode switch(to switch between raw recording and text-to speech). 

The software is just an index.html file to display the program in the browser, and an app.py file that controls the functionality. For transcription mode, it feeds raw audio to OpenAI's Whisper model, which returns a transcription that is displays in the browser. The recording can also be saved through the UI. 

The ESP32's role is quite simple: detect any touch to the copper pads, then send that information to the software program to handle actual recording/saving/playing/downloading.

For technical documentation, click here.

← [Back Home](index.html)
