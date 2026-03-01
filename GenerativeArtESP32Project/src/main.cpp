#include <Arduino.h>
// from BomSymbols in Icon Archive
#include "inlove.h"
// from bsd in Icon Archive
#include "goose.h"
// from Freepik in Icon Archive
#include "hug.h"
#include <TFT_eSPI.h>

TFT_eSPI tft = TFT_eSPI();

// sprites
TFT_eSprite background = TFT_eSprite(&tft);
TFT_eSprite txt = TFT_eSprite(&tft);

// Poem text from the poem "Wild Geese" by Mary Oliver
const char* line1 = "You do not have to be good.";
const char* words2[] = {"You","do","not","have","to","walk","on","your","knees", " ", "for", "a", "hundred", "miles", "through", "the", "desert", "repenting."};
const int words2Count = sizeof(words2) / sizeof(words2[0]);
const char* words3[] = {"You","only","have","to","let","the","soft","animal","of","your","body", "love","what","it","loves."};
const int words3Count = sizeof(words3) / sizeof(words3[0]);

// display variables
int scene;
int xPos;
int yOffset;
int word3Index;
unsigned long lastWordMs;
uint16_t currentWordColor;
const uint16_t palette[] = {
  TFT_RED, TFT_ORANGE, TFT_YELLOW, TFT_GREEN, TFT_BLUE, TFT_PINK, TFT_BLACK, TFT_WHITE
};
const int paletteCount = sizeof(palette) / sizeof(palette[0]);
int whichImage;
unsigned long scene3StartMs;

void startScene(int newScene) {
  scene = newScene;
  if (scene == 0) {
    xPos = tft.width();      // start off-screen right
  } else if(scene == 1) {
    yOffset = 0;             // start at "normal" position (bottom aligned stack)
  } else if(scene == 2) {
    word3Index = 0;
    lastWordMs = millis();
    currentWordColor = palette[random(paletteCount)];
  } else if(scene == 3) {
    whichImage = random(3); 
    scene3StartMs = millis();
  }
}

void setup() {
  tft.init();
  tft.setSwapBytes(true);
  tft.setRotation(2);

  background.createSprite(tft.width(), tft.height());
  background.setTextWrap(false);
  background.setSwapBytes(true);
  txt.createSprite(320, 70);
  txt.setTextWrap(false);

  randomSeed(micros());

  startScene(0);
}

void loop() {
  if(scene == 0) {
    background.fillSprite(TFT_GREEN);

    txt.fillSprite(TFT_BLACK);
    txt.setTextColor(TFT_BLUE, TFT_BLACK);
    txt.drawString(line1, 0, 0, 4);
    txt.pushToSprite(&background, xPos, 80, TFT_BLACK);

    xPos -= 2;

    int textW = txt.textWidth(line1, 4);
    if (xPos < -textW) {
      startScene(1);
    }

  } else if (scene == 1) {
    background.fillSprite(TFT_BLACK);
    background.setTextColor(TFT_BLUE, TFT_BLACK);

    int lineHeight = background.fontHeight(4) + 6;

    for (int i = 0; i < words2Count; i++) {
      int y = (tft.height() - background.fontHeight(4)) + i * lineHeight - yOffset;
      background.drawString(words2[i], 10, y, 4);
    }

    yOffset += 2;

    if (yOffset > (tft.height() + (words2Count*lineHeight))) {
      startScene(2);
    }
  } else if(scene == 2) {
    background.fillSprite(TFT_PURPLE);

    unsigned long now = millis();
    if (now - lastWordMs >= 700) {
      lastWordMs = now;
      word3Index++;
      if (word3Index >= words3Count) {
        startScene(3); 
        return;
      }

      currentWordColor = palette[random(paletteCount)];
    }

    background.setTextColor(currentWordColor, TFT_PURPLE);

    const char* w = words3[word3Index];
    int textW = background.textWidth(w, 4);
    int textH = background.fontHeight(4);

    int x = (tft.width() - textW) / 2;
    int y = (tft.height() - textH) / 2;

    background.drawString(w, x, y, 4);
  } else if (scene == 3) {
    background.fillSprite(TFT_PINK);

    int imgW = 128;
    int imgH = 128;
    int x = (tft.width()  - imgW) / 2;
    int y = (tft.height() - imgH) / 2;

    if (whichImage == 0) {
      background.pushImage(x, y, imgW, imgH, inlove); 
    } else if(whichImage == 1) {
      background.pushImage(x, y, imgW, imgH, goose); 
    } else if(whichImage == 2) {
      background.pushImage(x, y, imgW, imgH, hug); 
    }

    if (millis() - scene3StartMs >= 3000) {
      startScene(0);
    }
  }

  background.pushSprite(0,0);
}