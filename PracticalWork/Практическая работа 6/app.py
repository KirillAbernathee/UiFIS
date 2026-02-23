import tkinter as tk
import math

class Planet:
    def __init__(self, name, orbit_radius, speed, size, color, start_angle):
        self.name = name
        self.orbit_radius = orbit_radius
        self.speed = speed
        self.size = size
        self.color = color
        self.angle = math.radians(start_angle)

class SolarSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Солнечная система")
        self.root.geometry("900x700")
        
        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.center_x = self.root.winfo_width() // 2
        self.center_y = self.root.winfo_height() // 2
        self.zoom = 1.0
        self.speed_multiplier = 1.0
        self.paused = False
        self.base_scale = 30
        
        self.planets = []
        self.init_planets()
        
        self.root.bind('<Configure>', self.on_resize)
        self.root.bind('<MouseWheel>', self.on_mousewheel)
        self.root.bind('<space>', self.toggle_pause)
        self.root.bind('<Up>', self.increase_speed)
        self.root.bind('<Down>', self.decrease_speed)
        
        self.animate()
        
    def init_planets(self):
        self.planets = [
            Planet("Меркурий", 1.0, 0.05, 8, '#A9A9A9', 0),
            Planet("Венера", 1.5, 0.03, 10, '#FF8C00', 30),
            Planet("Земля", 2.0, 0.02, 11, '#1E90FF', 60),
            Planet("Марс", 2.5, 0.018, 9, '#CD5C5C', 90),
            Planet("Юпитер", 3.2, 0.008, 20, '#DEB887', 120),
            Planet("Сатурн", 4.0, 0.006, 17, '#F4A460', 150),
            Planet("Уран", 4.7, 0.004, 14, '#7FFFD4', 180),
            Planet("Нептун", 5.4, 0.003, 14, '#4169E1', 210)
        ]
        
    def on_resize(self, event):
        self.center_x = self.canvas.winfo_width() // 2
        self.center_y = self.canvas.winfo_height() // 2
        
    def on_mousewheel(self, event):
        if event.delta > 0:
            self.zoom *= 1.1
        else:
            self.zoom *= 0.9
        self.zoom = max(0.3, min(3.0, self.zoom))
        
    def toggle_pause(self, event):
        self.paused = not self.paused
        
    def increase_speed(self, event):
        self.speed_multiplier *= 1.2
        
    def decrease_speed(self, event):
        self.speed_multiplier *= 0.8
        
    def draw_stars(self):
        import random
        for _ in range(100):
            x = random.randint(0, self.canvas.winfo_width())
            y = random.randint(0, self.canvas.winfo_height())
            self.canvas.create_oval(x, y, x+2, y+2, fill='white', outline='')
            
    def draw_sun(self):
        sun_size = max(10, min(60, 40 * self.zoom))
        x0 = self.center_x - sun_size
        y0 = self.center_y - sun_size
        x1 = self.center_x + sun_size
        y1 = self.center_y + sun_size
        self.canvas.create_oval(x0, y0, x1, y1, fill='yellow', outline='orange', width=2)
        self.canvas.create_text(self.center_x, self.center_y - sun_size - 15, text='Солнце', fill='white', font=('Arial', 12))
        
    def draw_orbits(self):
        for planet in self.planets:
            radius = planet.orbit_radius * self.base_scale * self.zoom
            if radius < 10:
                continue
            x0 = self.center_x - radius
            y0 = self.center_y - radius
            x1 = self.center_x + radius
            y1 = self.center_y + radius
            self.canvas.create_oval(x0, y0, x1, y1, outline='#333333', width=1)
            
    def draw_planets(self):
        for planet in self.planets:
            if not self.paused:
                planet.angle += planet.speed * self.speed_multiplier * 0.02
                
            radius = planet.orbit_radius * self.base_scale * self.zoom
            x = self.center_x + math.cos(planet.angle) * radius
            y = self.center_y + math.sin(planet.angle) * radius
            
            size = max(4, min(40, planet.size * self.zoom))
            
            x0 = x - size
            y0 = y - size
            x1 = x + size
            y1 = y + size
            
            self.canvas.create_oval(x0, y0, x1, y1, fill=planet.color, outline='white', width=1)
            self.canvas.create_text(x, y - size - 8, text=planet.name, fill='white', font=('Arial', 9))
            
    def draw_ui(self):
        status = "Paused" if self.paused else "Running"
        info = f"Status: {status} | Speed: {self.speed_multiplier:.1f}x | Zoom: {self.zoom:.1f}x"
        self.canvas.create_text(10, 10, text=info, fill='white', anchor='nw', font=('Arial', 10))
        self.canvas.create_text(10, 30, text="Space: Pause | Up/Down: Speed | Mouse Wheel: Zoom", fill='gray', anchor='nw', font=('Arial', 9))
        
    def animate(self):
        self.canvas.delete('all')
        self.draw_stars()
        self.draw_sun()
        self.draw_orbits()
        self.draw_planets()
        self.draw_ui()
        self.root.after(20, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = SolarSystemApp(root)
    root.mainloop()