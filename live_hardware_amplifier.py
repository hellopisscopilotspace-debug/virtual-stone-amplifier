# Copyright (c) 2026 hellopisscopilotspace-debug
# All rights reserved. Licensed under GNU GPL v3.0
# Smart Adaptive Engine: Universal Hardware-Agnostic Optimizer

import time
import random
import subprocess
import psutil
import sys
import os
from collections import deque

class UniversalHardwareBridge:
    def __init__(self):
        self.os_type = sys.platform
        self.has_accelerator = self._check_generic_accelerator()
        print(f"[INIT] Platform Substrate: {self.os_type}")
        print(f"[INIT] Hardware Accelerator Detected: {self.has_accelerator}")

    def _check_generic_accelerator(self):
        """Universally scans for any compute accelerator without vendor-lock."""
        commands = [
            ["nvidia-smi"],       # Architecture Type A
            ["rocm-smi"],         # Architecture Type B
            ["clinfo"],           # Universal OpenCL Substrate
            ["system_profiler", "SPDisplaysDataType"] # Unix/POSIX Substrate
        ]
        
        for cmd in commands:
            try:
                with open(os.devnull, 'w') as devnull:
                    subprocess.run(cmd, stdout=devnull, stderr=devnull, check=True)
                return True
            except:
                continue
        return False

    def get_cpu(self):
        """Returns total main processor load in %."""
        return psutil.cpu_percent(interval=0.05)

    def get_ram(self):
        """Returns system memory utilization ratio (0.0 to 1.0)."""
        mem = psutil.virtual_memory()
        return mem.percent / 100.0

    def get_temperature(self):
        """Universal substrate thermal telemetry collector."""
        try:
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name in temps:
                        if temps[name]:
                            temp = temps[name][0].current
                            # Normalize (30°C - 100°C) to 0.0 - 1.0 range
                            return max(0.0, min(1.0, (temp - 30) / 70))
        except:
            pass
        # Indirect software-derived metric if direct sensor bus access is restricted
        return max(0.1, min(0.9, (self.get_cpu() / 100.0) * 1.1))

    def get_accelerator_usage(self):
        """Cross-platform utilization tracker for any secondary computational unit."""
        if not self.has_accelerator:
            return 0.0
            
        tools = [
            (["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"], 100.0),
            (["rocm-smi", "--showuse"], 100.0)
        ]
        
        for cmd, scale in tools:
            try:
                result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
                lines = result.decode().strip().split("\n")[0]
                # Strip text fluff, isolate numerical telemetry digits
                digits = ''.join(c for c in lines if c.isdigit() or c == '.')
                if digits:
                    return float(digits) / scale
            except:
                continue
        return 0.0


class SmartAdaptiveEngine:
    def __init__(self):
        self.hw = UniversalHardwareBridge()
        self.memory = deque(maxlen=30)
        self.best_score = 0.0
        self.best_genome = None
        
        # Hardware-agnostic initialization genome
        self.genome = {
            "w": 3,               # Computational step width
            "c": 128,             # Virtual layer cache capacity (MB)
            "accel_bias": 0.5 if self.hw.has_accelerator else 0.0,
            "mutation_rate": 0.25
        }

    def measure(self, genome):
        cpu = self.hw.get_cpu()
        ram = self.hw.get_ram()
        accel = self.hw.get_accelerator_usage()
        therm = self.hw.get_temperature()

        # Vendor-agnostic synthetic performance calculation
        accel_factor = (accel * 100 * genome["accel_bias"]) if self.hw.has_accelerator else 0.0
        speed = (100 - cpu) + accel_factor
        
        return cpu, ram, accel, speed, therm

    def score(self, cpu, ram, speed, therm, genome):
        raw = speed
        # Pragmatic hardware protection penalty matrix
        penalty = ((cpu / 100) * 0.50 + ram * 0.30 + therm * 0.70)
        result = raw * (1.0 - penalty)
        
        # Anti-collapse protection protocol (runtime self-preservation instinct)
        if result < 1:
            result = 1 + speed * 0.01
            
        return round(result, 2)

    def mutate(self, genome):
        new = genome.copy()
        
        if self.hw.has_accelerator and random.random() < genome["mutation_rate"]:
            new["accel_bias"] += random.uniform(-0.15, 0.15)
            new["accel_bias"] = max(0.0, min(1.5, new["accel_bias"]))

        if random.random() < genome["mutation_rate"]:
            new["mutation_rate"] += random.uniform(-0.05, 0.05)
            new["mutation_rate"] = max(0.05, min(0.60, new["mutation_rate"]))
            
        if random.random() < genome["mutation_rate"]:
            new["w"] = random.choice([2, 3, 4])
            new["c"] = random.choice([64, 128, 192, 256])
            
        return new

    def selection(self, score, genome):
        if score > self.best_score:
            self.best_score = score
            self.best_genome = genome.copy()
        
        if len(self.memory) > 10:
            stability = max(self.memory) - min(self.memory)
            # Homeostatic chaos detection & rolling restoration
            if stability > 130:
                if self.best_genome:
                    print("\n[SYSTEM ROLLBACK] Unstable substrate telemetry. Reverting to best stable genome.\n")
                    self.genome = self.best_genome.copy()
                    self.memory.clear()

    def run(self):
        print("\n" + "="*75)
        print(" UNIVERSAL ADAPTIVE ENGINE (HARDWARE-AGNOSTIC RUNTIME)")
        print("="*75 + "\n")
        
        while True:
            try:
                self.genome = self.mutate(self.genome)
                cpu, ram, accel, speed, therm = self.measure(self.genome)
                s = self.score(cpu, ram, speed, therm, self.genome)
                self.memory.append(s)
                self.selection(s, self.genome)

                print(
                    f"CPU:{cpu:5.1f}% | "
                    f"RAM:{ram:.2f} | "
                    f"ACCEL:{accel:.2f} | "
                    f"THERM:{therm:.2f} | "
                    f"W:{self.genome['w']} | "
                    f"C:{self.genome['c']:3}MB | "
                    f"BIAS:{self.genome['accel_bias']:.2f} | "
                    f"SCORE:{s:7.2f} | "
                    f"BEST:{self.best_score:7.2f}"
                )
                time.sleep(0.25)
                
            except KeyboardInterrupt:
                print("\n\n[EXIT] Optimization cycle interrupted by operator.")
                if self.best_genome:
                    print(f"[RESULT] Optimal discovered architecture genome: {self.best_genome}")
                break

if __name__ == "__main__":
    engine = SmartAdaptiveEngine()
    engine.run()
                break

if __name__ == "__main__":
    engine = SmartAdaptiveEngine()
    engine.run()
