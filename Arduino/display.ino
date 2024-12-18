#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

int lineHeight = 10;  // Height of text line, adjust based on font size
int currentY = 0;      // Current y position of cursor

int buzzer = 5; // Buzzer pin number

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Initialize with the I2C addr 0x3C
    Serial.println(F("SSD1306 allocation failed"));
    for(;;); // Don't proceed, loop forever
  }
  display.clearDisplay();
  display.setTextSize(1); // Normal 2:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.cp437(true); // Use full 256 char 'Code Page 437' font
  pinMode(buzzer, OUTPUT); // Set the buzzer pin as an output
}

void loop() {
  if (Serial.available() > 0) { // Pyserial is sending information
    String message = Serial.readStringUntil('\n'); // Read the incoming data until newline
    if(currentY + lineHeight > SCREEN_HEIGHT) { // Check if there is space for another line
      display.clearDisplay(); // Clear display if no space for new line
      currentY = 0; // Reset cursor to top of the display
    }
    
    tone(buzzer, 1000, 300); // Activate buzzer at 1000 Hz for 300 milliseconds

    display.setCursor(0, currentY); // Set cursor to new line
    display.println(message); // Print the message on the display
    display.display(); // Actually draw everything we've written
    
    currentY += lineHeight; // Move cursor down to next line
  }
}
