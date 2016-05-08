const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int analogOutPin = 9; // Analog output pin that the LED is attached to


#define COUNT 50

int sensorValues[COUNT] = {0};        // value read from the pot
long int sensorTimes[COUNT] = {0};        // value read from the pot

int sensorValue = 0;

char guardado_minimo = 0;


int valor1, valor2;
long int tiempo1, tiempo2;

void append_value(int *buffer, int value) {
  int i;
  for(i=COUNT-1; i>0; i--)
    sensorValues[i] = sensorValues[i-1];
  sensorValues[0] = value;
}

void append_time(long int *buffer, long int value) {
  int i;
  for(i=COUNT-1; i>0; i--)
    sensorTimes[i] = sensorTimes[i-1];
  sensorTimes[0] = value;
}

char busca(int *buffer) {
  int max_bucle = buffer[0];
  int count_min_bucle = 1;
  int min_bucle = buffer[0];
  int count_max_bucle = 1;

  int i;
  for (i=1; i<COUNT; i++) {
    if (buffer[i] < min_bucle) {
      min_bucle = buffer[i];
      count_min_bucle = 1;
    } else if (buffer[i] == min_bucle) {
      count_min_bucle++;
    }
    if (buffer[i] > max_bucle) {
      max_bucle = buffer[i];
      count_max_bucle = 1;
    } else if (buffer[i] == max_bucle) {
      count_max_bucle++;
    }
  }
  
  /* Serial.print("X ");
  Serial.print(min_bucle);
      Serial.print(" ");
  Serial.print(max_bucle);
      Serial.print(" ");
  Serial.println(buffer[COUNT/2]); */

  if (min_bucle == buffer[COUNT/2] && count_min_bucle == 1)
    return 1;
  if (max_bucle == buffer[COUNT/2] && count_max_bucle == 1)
    return 2;
  return 0;
}

void setup() {
  Serial.begin(115200); 
}

void loop() {
   int analog = analogRead(analogInPin);
   long int tiempo = millis();
   
   append_value(sensorValues, analog);
   append_time(sensorTimes, tiempo);

   char resultado = busca(sensorValues);
   
   if (resultado == 1 && guardado_minimo == 0) {
      valor1 = sensorValues[COUNT/2];
      tiempo1 = sensorTimes[COUNT/2];   
      guardado_minimo = 1;   
   } else if (resultado == 2 && guardado_minimo == 1) {
      valor2 = sensorValues[COUNT/2];
      tiempo2 = sensorTimes[COUNT/2];    
      guardado_minimo = 0;  
      Serial.print(tiempo1);
      Serial.print(" ");
      Serial.print(valor1);
      Serial.print(" ");
      Serial.print(tiempo2);
      Serial.print(" ");
      Serial.println(valor2);
   }
   
   //delay(10); 
 
 }
