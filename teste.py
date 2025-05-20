import pyautogui
import time

print("Mova o mouse até o canto superior esquerdo da área desejada...")
time.sleep(5)  # te dá tempo de posicionar
print("Posição inicial:", pyautogui.position())

time.sleep(5)
print("Agora mova o mouse até o canto inferior direito da área...")
time.sleep(5)
print("Posição final:", pyautogui.position())
