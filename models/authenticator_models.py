#!/usr/bin/env python3
"""
Authenticator Models - Sistema de Autenticación
"""

import os
import sys
import getpass
import hashlib
import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, simpledialog


class DesktopAuthenticator:
    """Autenticador para aplicación de escritorio"""
    
    def __init__(self):
        self.config_file = Path("auth_config.json")
        self.authenticated = False
    
    def authenticate_user_desktop(self):
        """Solicitar PIN en ventana de escritorio"""
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        
        try:
            pin = simpledialog.askstring(
                "Autenticación", 
                "Ingrese su PIN:",
                show='*'
            )
            
            if pin:
                if self.validate_pin(pin):
                    messagebox.showinfo("Éxito", "Autenticación exitosa")
                    self.authenticated = True
                    root.destroy()
                    return True
                else:
                    messagebox.showerror("Error", "PIN incorrecto")
            
            root.destroy()
            return False
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en autenticación: {e}")
            root.destroy()
            return False
    
    def validate_pin(self, pin):
        """Validar PIN (por ahora simulado)"""
        # Opción 1: PIN fijo para desarrollo
        return pin == "1234"
        
        # Opción 2: PIN guardado (descomenta para usar)
        # return self.check_stored_pin(pin)
    
    def setup_pin(self):
        """Configurar PIN por primera vez"""
        root = tk.Tk()
        root.withdraw()
        
        pin = simpledialog.askstring(
            "Configurar PIN", 
            "Cree su PIN (4 dígitos):",
            show='*'
        )
        
        if pin and len(pin) == 4 and pin.isdigit():
            self.store_pin(pin)
            messagebox.showinfo("Éxito", "PIN configurado correctamente")
            root.destroy()
            return True
        else:
            messagebox.showerror("Error", "PIN debe ser 4 dígitos")
            root.destroy()
            return False
    
    def store_pin(self, pin):
        """Guardar PIN encriptado"""
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        config = {"pin_hash": hashed_pin}
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f)
    
    def check_stored_pin(self, pin):
        """Verificar PIN guardado"""
        if not self.config_file.exists():
            return False
        
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        return config.get("pin_hash") == hashed_pin


def authenticate_user():
    """Función legacy para compatibilidad"""
    auth = DesktopAuthenticator()
    return auth.authenticate_user_desktop()