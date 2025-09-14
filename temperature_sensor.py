import random
import time

def generate_temperature_data(queue):
    while True:
        temperature = random.uniform(15.0, 35.0)  # Satunnainen lämpötila Celsius-asteina
        data = {"temperature": temperature}
        
        # Lähetä data pääprosessille
        queue.put(data)
        
        print(f"Generated temperature data: {data}")
        time.sleep(20)  # Odota 20 sekunttia ennen seuraavaa mittausta
