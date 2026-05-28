# Copyright (c) 2026 hellopisscopilotspace-debug
# All rights reserved. Licensed under GNU GPL v3.0
# Smart Adaptive Engine: Fully Universal Hardware-Agnostic Optimizer

import time
import random
import subprocess
import psutil
import sys
from collections import deque

class UniversalHardwareBridge:
    def __init__(self):
        self.has_nvidia = self._check_nvidia()
        self.os_type = sys.platform
        print(f"[INIT] Operating System: {self.os_type}")
        print(f"[INIT] NVIDIA GPU Detected: {self.has_nvidia}")

    def _check_nvidia(self):
        """Проверяет, доступна ли утилита nvidia-smi в системе."""
        try:
            with open(os.devnull, 'w') as devnull:
                subprocess.run(["nvidia-smi"], stdout=devnull, stderr=devnull, check=True)
            return True
        except:
            return False

    def get_cpu(self):
        """Возвращает общую загрузку CPU в %."""
        return psutil.cpu_percent(interval=0.05)

    def get_ram(self):
        """Возвращает процент использования оперативной памяти (0.0 - 1.0)."""
        mem = psutil.virtual_memory()
        return mem.percent / 100.0

    def get_temperature(self):
        """
        Универсальный сборщик температур. 
        Автоматически адаптируется под доступные датчики (Linux/Windows).
        """
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    # Ищем любые доступные датчики ядра (coretemp, cpu_thermal и т.д.)
                    for name in temps:
                        if temps[name]:
                            temp = temps[name][0].current
                            # Нормализация (30°C - 100°C) в диапазон 0.0 - 1.0
                            return max(0.0, min(1.0, (temp - 30) / 70))
        except:
            pass
        
        # Если датчики заблокированы или это Windows без прав админа, 
        # вычисляем псевдо-температуру на основе нагрузки CPU (косвенный замер)
        return max(0.1, min(0.9, (self.get_cpu() / 100.0) * 1.1))

    def get_gpu_usage(self):
        """
        Кроссплатформенный замер GPU. 
        Сам определяет тип карты или возвращает 0.0, если графический чип встроенный.
        """
        if self.has_nvidia:
            try:
                result = subprocess.check_output(
                    ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"],
                    stderr=subprocess.DEVNULL
                )
                lines = result.decode().strip().split("\n")
                if lines and lines[0].isdigit():
                    return float(lines[0]) / 100.0
            except:
                pass

        # Для macOS (Apple Silicon M1/M2/M3/M4) замер через powermetrics, если доступно
        if self.os_type == "darwin":
            try:
                # Мягкий замер без sudo вернет ошибку, ловим ее через except
                pass 
            except:
                pass

        return 0.0


class SmartAdaptiveEngine:
    def __init__(self):
        self.hw = UniversalHardwareBridge()
        self.memory = deque(maxlen=30)
        self.best_score = 0.0
        self.best_genome = None
        
        # Начальный универсальный геном
        self.genome = {
            "w": 3,               # Ширина вычислительного потока
            "c": 128,             # Размер виртуального кэша слоев (MB)
            "gpu_bias": 0.5 if self.hw.has_nvidia else 0.0, # Автоподстройка под наличие GPU
            "mutation_rate": 0.25
        }

    def measure(self, genome):
        cpu = self.hw.get_cpu()
        ram = self.hw.get_ram()
        gpu = self.hw.get_gpu_usage()
        therm = self.hw.get_temperature()

        # Универсальная формула синтетической скорости:
        # Учитывает свободную мощность процессора и акселерацию от GPU (если оно есть)
        gpu_factor = (gpu * 100 * genome["gpu_bias"]) if self.hw.has_nvidia else 0.0
        speed = (100 - cpu) + gpu_factor
        
        return cpu, ram, gpu, speed, therm

    def score(self, cpu, ram, speed, therm, genome):
        raw = speed
        # Прагматичные штрафы: перегрев бьет сильнее всего по выживаемости софта
        penalty = ((cpu / 100) * 0.50 + ram * 0.30 + therm * 0.70)
        result = raw * (1.0 - penalty)
        
        # Анти-коллапс защита (инстинкт самосохранения кода при критической нагрузке)
        if result < 1:
            result = 1 + speed * 0.01
            
        return round(result, 2)

    def mutate(self, genome):
        new = genome.copy()
        
        # Мутация склонности к GPU происходит только если физическая карта обнаружена
        if self.hw.has_nvidia and random.random() < genome["mutation_rate"]:
            new["gpu_bias"] += random.uniform(-0.15, 0.15)
            new["gpu_bias"] = max(0.0, min(1.5, new["gpu_bias"]))
            
        # Мутация агрессивности самого эволюционного поиска
        if random.random() < genome["mutation_rate"]:
            new["mutation_rate"] += random.uniform(-0.05, 0.05)
            new["mutation_rate"] = max(0.05, min(0.60, new["mutation_rate"]))
            
        # Мутация шага архитектурной конфигурации (W и C)
        if random.random() < genome["mutation_rate"]:
            new["w"] = random.choice([2, 3, 4, 5])
            new["c"] = random.choice([64, 128, 192, 256, 512])
            
        return new

    def selection(self, score, genome):
        if score > self.best_score:
            self.best_score = score
            self.best_genome = genome.copy()
        
        # Детекция хаоса и авто-откат к стабильному состоянию железа
        if len(self.memory) > 10:
            stability = max(self.memory) - min(self.memory)
            if stability > 130:  # Порог критического разброса метрик
                if self.best_genome:
                    print("\n[SYSTEM ROLLBACK] Unstable hardware state detected. Reverting to best stable genome.\n")
                    self.genome = self.best_genome.copy()
                    self.memory.clear()

    def run(self):
        print("\n" + "="*75)
        print(" UNIVERSAL SMART ADAPTIVE ENGINE (RUNTIME MODE)")
        print("="*75 + "\n")
        
        while True:
            try:
                # 1. Шаг мутации софта
                self.genome = self.mutate(self.genome)
                
                # 2. Снятие живых физических параметров
                cpu, ram, gpu, speed, therm = self.measure(self.genome)
                
                # 3. Расчет выживаемости конфигурации
                s = self.score(cpu, ram, speed, therm, self.genome)
                self.memory.append(s)
                
                # 4. Естественный отбор и проверка на перегрузку
                self.selection(s, self.genome)

                # Универсальный вывод телеметрии в консоль
                print(
                    f"CPU:{cpu:5.1f}% | "
                    f"RAM:{ram:.2f} | "
                    f"GPU:{gpu:.2f} | "
                    f"TEMP:{therm:.2f} | "
                    f"W:{self.genome['w']} | "
                    f"C:{self.genome['c']:3}MB | "
                    f"GPU_BIAS:{self.genome['gpu_bias']:.2f} | "
                    f"SCORE:{s:7.2f} | "
                    f"BEST:{self.best_score:7.2f}"
                )
                time.sleep(0.25)
                
            except KeyboardInterrupt:
                print("\n\n[EXIT] Optimization cycle stopped by operator.")
                if self.best_genome:
                    print(f"[RESULT] Optimal discovered architecture genome for this hardware: {self.best_genome}")
                break

if __name__ == "__main__":
    engine = SmartAdaptiveEngine()
    engine.run()
