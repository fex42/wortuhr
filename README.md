# Wortuhr für 3D Drucker

Dies ist meine Variante der Wortuhr, bei der ich Wert auf möglichst einfachen Bau und gute Optik gelegt habe. Außerdem ist es für mich ein kleines Übungsprojekt um etwas "hands on" Erfahrung mit [build123d](https://build123d.readthedocs.io/) zu sammeln. Man sehe mir nach, wenn der Code nicht besonders eleganz ist (ich bin weder mit Python noch mit build123d besonders gut.)

Build123d installiert man am besten direkt über das "OCP CAD Viewer" Plugin aus Visual Studio Code. Das ergibt eine sehr nette Entwicklungsumgebung mit 3D-Previewer.

Um die Wortuhr zu bauen, druckt man die entstehenden Teile. Mehrfach zu druckende Teile sind tragen im Dateinamen die Anzahl "_x2", "_x4" oder "_x110", d.h. diese Teile müssen zwei, vier oder 110 mal gedruckt werden.

# Hinweise zum Druck der Frontplatte

Ich habe die Frontplatte in drei Varianten gedruckt. Man kann die ersten beiden Schichten weiß oder durchsichtig drucken, dazu sollte man den Parameter "diffusor_th" auf 0,4 erhöhen, damit er zwei Schichten umfasst. Am besten gefällt mir aber der Druck, bei der die erste Schicht 0,2mm schwarzem PLA ist. Die Schicht ist dann so dünn, dass die LEDs durchscheinen, aber dunkle Buchstaben sind gar nicht zu sehen.

Druckt man die ersten beiden Schichten mit weißem PLA, wirkt dann braucht man keine Diffusoren drucken, die sind nur nötig, wenn man durchsichtiges oder komplett in Schwarz druckt und werden von den Innenseite einfach eingesteckt, kleben ist bei mir nicht nötig, kommt aber ggf. auf den Drucker bzw. die Filamentkalibrierung an.

Will man die erste(n) Schichten homogen durchgängig drucken, kann man das im (Orca-)Slicer mit einer Modifier-Box erreichen, bei der man die Anzahl von Top-Layern auf 0 stellt. Macht man das nicht, generiert der Slicer einen Druck, wo die zweite Schicht zwar durchgehend ist, um die Buchstaben aber Wandlinien gedruckt sind, was man als Artefakte erkennen kann.

## Liste zusätzlich benötigter Teile

Neben den Druckteilen braucht man noch folgende Bauteile

- 12 x Einschmelzmutter M3x4.5x4.5 (https://de.aliexpress.com/item/1005004629314742.html)
- 12 x Linsenschrauben M8x6 oder M8x8
- 1 x ESP8266 Board (ich bevorzuge das kleine Wemos D1 Mini lite, es geht aber auch eine NodeMCU)
- 1 x WS2812B RGB LED Stripe (60 LED/m, IP30)
- 1 x USB-C Stromversorgungs-Stecker (https://de.aliexpress.com/item/1005007148475800.html)

# Firmware

Es gibt viele Firmware-Varianten für die Wortuhr. Ich habe diese hier benutzt:

https://github.com/ESPWortuhr/Multilayout-ESP-Wordclock

Wenn man wie ich einen Wemos D1 Mini lite benutzt, muss man die platformio.ini Datei ergänzen, das habe ich in meinem Fork hier gemacht:

