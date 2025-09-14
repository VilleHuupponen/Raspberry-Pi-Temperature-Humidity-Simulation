import random
import time

def generate_humidity_data(queue):
    while True:
        humidity = random.uniform(30.0, 70.0)  # Satunnainen kosteusprosentti
        data = {"humidity": humidity}
        
        # Lähetä data pääprosessille
        queue.put(data)
        
        print(f"Generated humidity data: {data}")
        time.sleep(20)  # Odota 20 sekunttia ennen seuraavaa mittausta
