import pyautogui
import time


print("Posicione o mouse no **lado esquerdo** e aguarde 3 segundos...")
print(1)
time.sleep(0.5)
print(2)
time.sleep(0.5)
print(3)
time.sleep(0.5)

print(4)
time.sleep(0.5)

print(5)



time.sleep(3)
x1, y1 = pyautogui.position()
print(f"Lado esquerdo capturado: ({x1}, {y1})")

print("Agora posicione o mouse no **lado direito** e aguarde 3 segundos...")
print(1)
time.sleep(0.5)

print(2)
time.sleep(0.5)

print(3)
time.sleep(0.5)

print(4)
time.sleep(0.5)

print(5)
time.sleep(3)
x2, y2 = pyautogui.position()
print(f"Lado direito capturado: ({x2}, {y2})")
