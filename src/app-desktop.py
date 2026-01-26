
"""
AI Document Trainer - Aplicación de Escritorio
Interfaz de escritorio nativa para consultar IA entrenada
"""

# ================================
# IMPORTACIONES BÁSICAS
# ================================
import os
import sys
import logging
from datetime import datetime
from pathlib import Path

# ================================
# INTERFAZ DESKTOP
# ================================
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk

# ================================
# UTILIDADES
# ================================
from typing import List, Dict, Optional, Union
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
from authenticator_models import DesktopAuthenticator


def __init__():
    """Inicialización del módulo de consulta desktop"""
    print("Iniciando aplicación de escritorio...")
    auth = DesktopAuthenticator()
    if not auth.authenticate_user_desktop():
        print("Autenticación fallida. Saliendo...")
        sys.exit(1)
    setup_logging()


def setup_logging():
    """Configurar sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('desktop_app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


class AIDesktopChat:
    """Aplicación de escritorio para chat con IA"""
    
    def __init__(self):
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.last_search_results = {}  # Guardar resultados de la última búsqueda
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interfaz de usuario"""
        self.root.title("AI Document Trainer - Consulta")
        self.root.geometry("900x700")
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="AI Document Trainer", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Área de respuesta (arriba)
        response_label = ctk.CTkLabel(
            main_frame, 
            text="Respuesta:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        response_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.response_text = ctk.CTkTextbox(
            main_frame,
            height=300,
            font=ctk.CTkFont(size=12)
        )
        self.response_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.response_text.insert("1.0", "Aquí aparecerá la respuesta de la IA...")
        
        # Frame para el prompt
        prompt_frame = ctk.CTkFrame(main_frame)
        prompt_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Label del prompt
        prompt_label = ctk.CTkLabel(
            prompt_frame, 
            text="Tu pregunta:", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        prompt_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        # Campo de texto para prompt
        self.prompt_entry = ctk.CTkTextbox(
            prompt_frame,
            height=80,
            font=ctk.CTkFont(size=12)
        )
        self.prompt_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Botón de enviar
        self.send_button = ctk.CTkButton(
            prompt_frame,
            text="Enviar Pregunta",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.send_prompt
        )
        self.send_button.pack(pady=(0, 20))
        
        # Bind Enter para enviar
        self.prompt_entry.bind("<Control-Return>", lambda e: self.send_prompt())
        
        # Status bar
        self.status_label = ctk.CTkLabel(
            main_frame, 
            text="Estado: Listo para consultas",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(side="bottom", pady=(0, 10))
    
    def send_prompt(self):
        """Enviar prompt y obtener respuesta"""
        prompt = self.prompt_entry.get("1.0", "end-1c").strip()
        
        if not prompt:
            messagebox.showwarning("Advertencia", "Por favor ingrese una pregunta")
            return
        
        # Actualizar status
        self.status_label.configure(text="Estado: Procesando...")
        self.send_button.configure(state="disabled", text="Procesando...")
        self.root.update()
        
        try:
            # Aquí iría la lógica de la IA (por ahora simulamos)
            response = self.get_ai_response(prompt)
            
            # Mostrar respuesta
            self.response_text.delete("1.0", "end")
            self.response_text.insert("1.0", response)
            
            # Limpiar prompt
            self.prompt_entry.delete("1.0", "end")
            
            # Actualizar status
            self.status_label.configure(text="Estado: Respuesta generada")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar: {e}")
            self.status_label.configure(text="Estado: Error en procesamiento")
        
        finally:
            self.send_button.configure(state="normal", text="Enviar Pregunta")
    
    def get_ai_response(self, prompt):
        """Obtener respuesta de la IA usando la base de conocimiento Cisco"""
        import time
        import json
        import os
        import re
        
        time.sleep(1)  # Simular procesamiento
        
        # Detectar si es una solicitud de información detallada
        detail_match = re.match(r'^(\d+)$', prompt.strip())
        if detail_match:
            return self.get_detailed_info(detail_match.group(1))
        
        # Detectar patrones como "más info punto 4" o "info 4"
        info_match = re.search(r'(?:más?\s+info|info|detalle).*?(\d+)', prompt.lower())
        if info_match:
            return self.get_detailed_info(info_match.group(1))
        
        try:
            # Cargar base de conocimiento Cisco
            knowledge_path = os.path.join("models", "cisco_knowledge_base.json")
            if not os.path.exists(knowledge_path):
                return "⚠️ Base de conocimiento no encontrada. Ejecuta primero el entrenamiento."
            
            with open(knowledge_path, 'r', encoding='utf-8') as f:
                cisco_data = json.load(f)
            
            prompt_lower = prompt.lower()
            
            # Filtrar comandos reales (que empiecen con comandos conocidos)
            real_commands = []
            for cmd in cisco_data['commands']:
                command_text = cmd['command'].strip()
                # Filtrar comandos que realmente parecen comandos Cisco
                if (command_text.startswith(('show ', 'configure ', 'interface ', 'router ', 'access-list', 'enable', 'no ', 'ip ')) 
                    and len(command_text) < 200  # No muy largos
                    and not any(word in command_text.lower() for word in ['page', 'figure', 'chapter', 'document', 'illustration'])):
                    
                    # Verificar relevancia con el prompt
                    if any(word in command_text.lower() for word in prompt_lower.split()):
                        real_commands.append(command_text)
            
            # Buscar configuraciones relevantes
            relevant_configs = []
            for config in cisco_data['configurations']:
                config_text = config['config'].strip()
                if (len(config_text) < 300 
                    and any(word in config_text.lower() for word in prompt_lower.split())
                    and not any(word in config_text.lower() for word in ['page', 'figure', 'chapter'])):
                    relevant_configs.append(config_text)
            
            # Buscar troubleshooting específico
            relevant_troubleshoot = []
            for trouble in cisco_data['troubleshooting']:
                trouble_text = trouble['issue'].strip()
                if (len(trouble_text) < 300 
                    and any(word in trouble_text.lower() for word in prompt_lower.split())
                    and not any(word in trouble_text.lower() for word in ['page', 'figure'])):
                    relevant_troubleshoot.append(trouble_text)
            
            # Generar respuesta mejorada
            response_parts = []
            
            # Respuestas específicas para consultas comunes
            if 'show interface' in prompt_lower:
                response_parts.append("🤖 Te explico cómo verificar el estado de las interfaces:")
                response_parts.append("")
                response_parts.append("🔧 GUÍA: VERIFICAR INTERFACES DE RED")
                response_parts.append("=" * 45)
                response_parts.append("")
                response_parts.append("📋 PASO 1: Conectar al ASA")
                response_parts.append("   → Abrir terminal/putty")
                response_parts.append("   → IP del ASA en el navegador para ASDM")
                response_parts.append("")
                response_parts.append("🔍 PASO 2: Ver TODAS las interfaces")
                response_parts.append("   → En CLI: show interface")
                response_parts.append("   → En ASDM: Monitoring > Interfaces")
                response_parts.append("")
                response_parts.append("📊 PASO 3: Ver resumen rápido")
                response_parts.append("   → Comando: show interface brief")
                response_parts.append("   → Verás: Nombre | IP | Estado | Protocolo")
                response_parts.append("")
                response_parts.append("🎯 PARA INTERFACE ESPECÍFICA:")
                response_parts.append("   → show interface GigabitEthernet0/0")
                response_parts.append("   → Cambia '0/0' por tu interfaz")
                response_parts.append("")
                response_parts.append("✅ QUÉ BUSCAR:")
                response_parts.append("   → 'line protocol is up' = Funcionando")
                response_parts.append("   → 'administratively down' = Deshabilitada")
                response_parts.append("   → Errores/drops altos = Problema")
                response_parts.append("")
            
            # Búsqueda especializada VPN
            elif any(word in prompt_lower for word in ['vpn', 'tunnel', 'ipsec', 'configurar vpn', 'tunel']):
                response_parts.append("🤖 ¡Perfecto! Te ayudo a configurar tu VPN paso a paso:")
                response_parts.append("")
                response_parts.append("🔐 GUÍA COMPLETA: CONFIGURACIÓN VPN SITE-TO-SITE")
                response_parts.append("=" * 55)
                
                response_parts.append("\n📋 PASO 1: Acceso a la Configuración")
                response_parts.append("   → Conecta a tu ASDM o CLI")
                response_parts.append("   → Ve al menú 'Configuration' > 'Site-to-Site VPN'")
                
                response_parts.append("\n🌐 PASO 2: Configuración de Red Local")
                response_parts.append("   → En la casilla 'Local Network', ingresa tu red interna")
                response_parts.append("   → Ejemplo: 192.168.1.0/24")
                response_parts.append("   → Máscara: 255.255.255.0")
                
                response_parts.append("\n🎯 PASO 3: Configuración de Red Remota")
                response_parts.append("   → En la pestaña siguiente, ve a 'Remote Network'")
                response_parts.append("   → Casilla 'Remote IP': La IP pública del otro extremo")
                response_parts.append("   → Ejemplo: 203.0.113.5")
                response_parts.append("   → Red remota: 10.0.0.0/24")
                
                response_parts.append("\n🔑 PASO 4: Configuración de Autenticación")
                response_parts.append("   → Pestaña 'IKE Parameters'")
                response_parts.append("   → Campo 'Pre-shared Key': Ingresa tu clave secreta")
                response_parts.append("   → Ejemplo: MiClaveSegura123!")
                response_parts.append("   → Método: PSK (Pre-Shared Key)")
                
                response_parts.append("\n⚙️ PASO 5: Configuración de Cifrado")
                response_parts.append("   → Pestaña 'Encryption'")
                response_parts.append("   → Casilla 'Encryption': AES-256")
                response_parts.append("   → Casilla 'Authentication': SHA-256")
                response_parts.append("   → Grupo DH: 14 o superior")
                
                response_parts.append("\n🚀 PASO 6: Aplicar Configuración")
                response_parts.append("   → Pestaña 'Interface Assignment'")
                response_parts.append("   → Selecciona tu interfaz externa (outside)")
                response_parts.append("   → Botón 'Apply' para guardar")
                response_parts.append("   → Botón 'Send' para aplicar al ASA")
                
                response_parts.append("\n✅ VERIFICACIÓN:")
                response_parts.append("   → Comando: show crypto isakmp sa")
                response_parts.append("   → Comando: show crypto ipsec sa")
                response_parts.append("   → Estado debe mostrar 'QM_IDLE'")
                
                # Buscar comandos específicos para detalles técnicos
                vpn_items = []
                for cmd in cisco_data['commands']:
                    cmd_text = cmd['command'].lower()
                    if (any(word in cmd_text for word in ['site-to-site', 'crypto', 'isakmp', 'ipsec', 'vpn']) and 
                        len(cmd['command']) > 30):
                        vpn_items.append({
                            'title': cmd['command'][:70] + "..." if len(cmd['command']) > 70 else cmd['command'],
                            'content': cmd['command'],
                            'section': cmd.get('section', ''),
                            'line': cmd.get('line', 0),
                            'type': 'command'
                        })
                
                # Guardar para navegación
                self.last_search_results = {
                    'type': 'vpn_guide',
                    'items': vpn_items[:8]
                }
                
                if vpn_items:
                    response_parts.append("\n📚 COMANDOS TÉCNICOS DISPONIBLES:")
                    for i, item in enumerate(vpn_items[:5]):
                        response_parts.append(f"   {i+1}. {item['title']}")
                    response_parts.append("\n💡 Escribe un número para ver el comando completo")
                
            # Respuesta conversacional para NAT
            elif any(word in prompt_lower for word in ['nat', 'traduccion', 'translation']):
                response_parts.append("🤖 ¡Te ayudo con la configuración NAT! Es muy sencillo:")
                response_parts.append("")
                response_parts.append("🔄 GUÍA: CONFIGURACIÓN NAT EN CISCO ASA")
                response_parts.append("=" * 45)
                response_parts.append("")
                response_parts.append("📋 PASO 1: Acceder a la Configuración")
                response_parts.append("   → ASDM: Configuration > Firewall > NAT Rules")
                response_parts.append("   → CLI: enable > configure terminal")
                response_parts.append("")
                response_parts.append("🌍 PASO 2: NAT Dinámico (Múltiples IPs internas)")
                response_parts.append("   → Botón 'Add' > Dynamic NAT")
                response_parts.append("   → Original Address: Tu red interna (192.168.1.0/24)")
                response_parts.append("   → Translated Address: IP pública o pool")
                response_parts.append("   → Interface: outside")
                response_parts.append("")
                response_parts.append("🎯 PASO 3: NAT Estático (IP específica)")
                response_parts.append("   → Botón 'Add' > Static NAT")
                response_parts.append("   → Original IP: IP interna específica (192.168.1.10)")
                response_parts.append("   → Translated IP: IP pública específica (203.0.113.10)")
                response_parts.append("   → Interfaces: inside → outside")
                response_parts.append("")
                response_parts.append("⚙️ PASO 4: Port Address Translation (PAT)")
                response_parts.append("   → En 'Translated Address'")
                response_parts.append("   → Selecciona 'Interface' para usar la IP de la interfaz")
                response_parts.append("   → Automáticamente usará diferentes puertos")
                response_parts.append("")
                response_parts.append("🚀 PASO 5: Aplicar Configuración")
                response_parts.append("   → Botón 'Apply' para revisar reglas")
                response_parts.append("   → Botón 'Send' para aplicar al ASA")
                response_parts.append("   → Verificar en 'Monitoring' > 'NAT'")
                response_parts.append("")
                response_parts.append("✅ VERIFICACIÓN:")
                response_parts.append("   → Comando: show nat detail")
                response_parts.append("   → Comando: show xlate")
                response_parts.append("   → Las traducciones deben aparecer activas")
                response_parts.append("")
                response_parts.append("🎯 ¿Qué tipo específico de NAT necesitas configurar?")
                return "\n".join(response_parts)
            
            # Respuesta conversacional para Firewall
            elif any(word in prompt_lower for word in ['firewall', 'access-list', 'acl', 'regla', 'bloquear']):
                response_parts.append("🤖 ¡Excelente! Te guío para configurar reglas de firewall:")
                response_parts.append("")
                response_parts.append("🛡️ GUÍA: CONFIGURACIÓN REGLAS DE FIREWALL")
                response_parts.append("=" * 45)
                response_parts.append("")
                response_parts.append("📋 PASO 1: Acceso a Reglas")
                response_parts.append("   → ASDM: Configuration > Firewall > Access Rules")
                response_parts.append("   → CLI: enable > configure terminal")
                response_parts.append("")
                response_parts.append("🔒 PASO 2: Crear Access List")
                response_parts.append("   → Botón 'Add' > Access Rule")
                response_parts.append("   → Nombre: ej. 'INSIDE_TO_OUTSIDE'")
                response_parts.append("   → Interface: inside (origen) → outside (destino)")
                response_parts.append("")
                response_parts.append("🎯 PASO 3: Definir Tráfico Permitido")
                response_parts.append("   → Source: Red origen (192.168.1.0/24)")
                response_parts.append("   → Destination: 'any' o IP específica")
                response_parts.append("   → Service: HTTP, HTTPS, ANY, etc.")
                response_parts.append("   → Action: Permit o Deny")
                response_parts.append("")
                response_parts.append("⚙️ PASO 4: Configurar Servicios Específicos")
                response_parts.append("   → Para Web: TCP/80 (HTTP) y TCP/443 (HTTPS)")
                response_parts.append("   → Para Email: TCP/25 (SMTP), TCP/110 (POP3)")
                response_parts.append("   → Para FTP: TCP/21 (Control), TCP/20 (Data)")
                response_parts.append("")
                response_parts.append("🚀 PASO 5: Aplicar y Ordenar Reglas")
                response_parts.append("   → Las reglas se evalúan de arriba hacia abajo")
                response_parts.append("   → Más específicas arriba, generales abajo")
                response_parts.append("   → Botón 'Apply' → 'Send'")
                response_parts.append("")
                response_parts.append("✅ VERIFICACIÓN:")
                response_parts.append("   → Comando: show access-list")
                response_parts.append("   → Comando: show conn")
                response_parts.append("   → Probar conectividad desde cliente")
                response_parts.append("")
                response_parts.append("🎯 ¿Qué tipo de tráfico específico necesitas permitir/bloquear?")
                return "\n".join(response_parts)
            
            # Respuesta conversacional para routing
            elif any(word in prompt_lower for word in ['route', 'routing', 'ruta', 'enrutamiento']):
                response_parts.append("🤖 ¡Te ayudo con la configuración de rutas!")
                response_parts.append("")
                response_parts.append("🗺️ GUÍA: CONFIGURACIÓN DE RUTAS")
                response_parts.append("=" * 40)
                response_parts.append("")
                response_parts.append("📋 PASO 1: Acceso a Routing")
                response_parts.append("   → ASDM: Configuration > Device Setup > Routing")
                response_parts.append("   → CLI: enable > configure terminal")
                response_parts.append("")
                response_parts.append("🎯 PASO 2: Ruta por Defecto")
                response_parts.append("   → Botón 'Add' en Static Routes")
                response_parts.append("   → Network: 0.0.0.0")
                response_parts.append("   → Mask: 0.0.0.0")
                response_parts.append("   → Gateway: IP del router (ej: 192.168.1.1)")
                response_parts.append("   → Interface: outside")
                response_parts.append("")
                response_parts.append("📍 PASO 3: Ruta Específica")
                response_parts.append("   → Network: Red destino (ej: 10.0.0.0)")
                response_parts.append("   → Mask: Máscara (ej: 255.255.255.0)")
                response_parts.append("   → Gateway: Próximo salto")
                response_parts.append("   → Metric: Prioridad (menor = mejor)")
                response_parts.append("")
                response_parts.append("✅ VERIFICACIÓN:")
                response_parts.append("   → Comando: show route")
                response_parts.append("   → Verificar conectividad: ping")
                response_parts.append("")
                response_parts.append("🎯 ¿Qué red necesitas alcanzar?")
                return "\n".join(response_parts)
            
            if real_commands:
                response_parts.append("🔧 COMANDOS RELACIONADOS ENCONTRADOS:")
                # Eliminar duplicados y tomar los más relevantes
                unique_commands = list(set(real_commands))[:8]
                
                # Guardar para navegación si no hay búsqueda VPN activa
                if not any(word in prompt_lower for word in ['vpn', 'tunnel', 'ipsec']):
                    command_items = []
                    for cmd in unique_commands:
                        command_items.append({
                            'title': cmd[:70] + "..." if len(cmd) > 70 else cmd,
                            'content': cmd,
                            'section': '',
                            'line': 0,
                            'type': 'command'
                        })
                    
                    self.last_search_results = {
                        'type': 'commands',
                        'items': command_items
                    }
                
                for i, cmd in enumerate(unique_commands):
                    response_parts.append(f"{i+1}. {cmd}")
                
                if not any(word in prompt_lower for word in ['vpn', 'tunnel', 'ipsec']):
                    response_parts.append(f"\n💡 Escribe un número para ver detalles del comando")
                
                response_parts.append("")
            
            if relevant_configs:
                response_parts.append("⚙️ CONFIGURACIONES RELACIONADAS:")
                unique_configs = list(set(relevant_configs))[:5]
                for i, config in enumerate(unique_configs):
                    response_parts.append(f"{i+1}. {config}")
                response_parts.append("")
            
            if relevant_troubleshoot:
                response_parts.append("🔍 TROUBLESHOOTING:")
                unique_troubleshoot = list(set(relevant_troubleshoot))[:3]
                for i, trouble in enumerate(unique_troubleshoot):
                    response_parts.append(f"{i+1}. {trouble}")
                response_parts.append("")
            
            if not any([real_commands, relevant_configs, relevant_troubleshoot]):
                # Respuesta amigable cuando no encuentra resultados específicos
                response_parts.append(f"🤖 Busqué en todo el manual de Cisco ASA pero no encontré comandos específicos para: '{prompt}'")
                response_parts.append("")
                response_parts.append("💡 PERO PUEDO AYUDARTE CON:")
                response_parts.append("")
                
                suggestions = {
                    'interface': {
                        'desc': '🌐 Configuración de Interfaces',
                        'examples': ['show interface', 'interface configuration', 'ip address']
                    },
                    'route': {
                        'desc': '🗺️ Enrutamiento',
                        'examples': ['route add', 'default gateway', 'static route']
                    },
                    'access': {
                        'desc': '🛡️ Control de Acceso',
                        'examples': ['access-list', 'firewall rules', 'permit deny']
                    },
                    'nat': {
                        'desc': '🔄 Traducción de Direcciones',
                        'examples': ['nat configuration', 'port translation', 'static nat']
                    },
                    'vpn': {
                        'desc': '🔐 Redes Privadas Virtuales',
                        'examples': ['vpn setup', 'site to site', 'crypto map']
                    },
                    'monitor': {
                        'desc': '📊 Monitoreo y Diagnóstico',
                        'examples': ['show commands', 'debug', 'logging']
                    }
                }
                
                # Mostrar sugerencias relevantes
                found_suggestion = False
                for keyword, info in suggestions.items():
                    if keyword in prompt_lower:
                        response_parts.append(f"{info['desc']}:")
                        for example in info['examples']:
                            response_parts.append(f"   → Pregúntame: '{example}'")
                        found_suggestion = True
                        break
                
                if not found_suggestion:
                    response_parts.append("🔥 CONSULTAS POPULARES QUE PUEDO RESOLVER:")
                    response_parts.append("   → 'configurar vpn' - Guía paso a paso VPN")
                    response_parts.append("   → 'configurar nat' - Traducción de direcciones")
                    response_parts.append("   → 'configurar firewall' - Reglas de acceso")
                    response_parts.append("   → 'show interface' - Verificar interfaces")
                    response_parts.append("   → 'configurar route' - Configurar rutas")
                
                response_parts.append("")
                response_parts.append("💬 EJEMPLOS DE PREGUNTAS ESPECÍFICAS:")
                response_parts.append("   → '¿Cómo bloqueo una IP específica?'")
                response_parts.append("   → '¿Cómo configuro acceso remoto?'")
                response_parts.append("   → '¿Cómo verifico el estado de la VPN?'")
                response_parts.append("   → '¿Qué comando uso para ver conexiones activas?'")
                response_parts.append("")
                response_parts.append("🎯 ¡Pregúntame de forma específica y te daré una guía paso a paso!")
                response_parts.append("")
            
            response_parts.append("📊 Cisco ASA 9.14 Knowledge Base")
            response_parts.append(f"Total: {len(cisco_data['commands']):,} comandos disponibles")
            
            return "\n".join(response_parts)
            
        except Exception as e:
            return f"❌ Error al consultar base de conocimiento: {e}"
    
    def get_detailed_info(self, item_number):
        """Obtener información detallada de un elemento específico"""
        if not self.last_search_results or 'items' not in self.last_search_results:
            return "❌ No hay resultados de búsqueda anteriores. Realiza una búsqueda primero."
        
        try:
            item_num = int(item_number) - 1  # Convertir a índice base 0
            items = self.last_search_results['items']
            
            if 0 <= item_num < len(items):
                item = items[item_num]
                
                # Formatear respuesta detallada conversacional
                detail = f"🤖 ¡Aquí está toda la información del elemento {item_number}!\n\n"
                detail += f"📋 INFORMACIÓN COMPLETA - ELEMENTO {item_number}\n"
                detail += "=" * 60 + "\n\n"
                
                detail += f"📝 CONTENIDO COMPLETO:\n"
                detail += f"   {item['content']}\n\n"
                
                if item.get('section'):
                    detail += f"📂 SECCIÓN DEL MANUAL: {item['section']}\n\n"
                
                if item.get('line'):
                    detail += f"📄 Ubicación: Línea {item['line']} del manual\n\n"
                
                if item.get('description'):
                    detail += f"📋 DESCRIPCIÓN ADICIONAL:\n   {item['description']}\n\n"
                
                # Agregar explicación contextual según el tipo
                detail += "💡 EXPLICACIÓN PRÁCTICA:\n"
                if 'crypto' in item['content'].lower() or 'vpn' in item['content'].lower():
                    detail += "   → Este comando es parte de la configuración VPN\n"
                    detail += "   → Úsalo en el orden correcto con otros comandos VPN\n"
                    detail += "   → Verifica la conectividad después de aplicarlo\n\n"
                elif 'access-list' in item['content'].lower():
                    detail += "   → Esta regla de firewall controla el tráfico\n"
                    detail += "   → Aplícala en la interfaz correcta\n"
                    detail += "   → Las reglas se evalúan en orden de arriba hacia abajo\n\n"
                elif 'nat' in item['content'].lower():
                    detail += "   → Esta regla traduce direcciones IP\n"
                    detail += "   → Asegúrate de que las interfaces sean correctas\n"
                    detail += "   → Verifica con 'show xlate' después de aplicar\n\n"
                elif 'interface' in item['content'].lower():
                    detail += "   → Configuración de interfaz de red\n"
                    detail += "   → Verifica el estado con 'show interface'\n"
                    detail += "   → Asegúrate de que esté 'up' y 'up'\n\n"
                else:
                    detail += "   → Comando de configuración general\n"
                    detail += "   → Sigue las mejores prácticas de seguridad\n"
                    detail += "   → Prueba en entorno de desarrollo primero\n\n"
                
                detail += "🔧 CÓMO APLICARLO:\n"
                detail += "   1. Accede al CLI o ASDM del ASA\n"
                detail += "   2. Entra en modo configuración: 'configure terminal'\n"
                detail += "   3. Aplica el comando exactamente como se muestra\n"
                detail += "   4. Guarda la configuración: 'write memory'\n\n"
                
                detail += "🎯 ¿Necesitas ayuda con algún paso específico de este comando?\n"
                detail += "   Puedes preguntarme sobre otro número o hacer una nueva búsqueda."
                
                return detail
            else:
                return f"❌ Número inválido. Elige entre 1 y {len(items)}"
                
        except ValueError:
            return "❌ Formato de número inválido. Usa solo números (ej: 3)"

    def run(self):
        """Ejecutar aplicación"""
        self.root.mainloop()


def main():
    """Función principal para aplicación de escritorio"""
    print("=" * 60)
    print("AI DOCUMENT TRAINER - APLICACIÓN DESKTOP")
    print("=" * 60)
    print(f"Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Crear y ejecutar aplicación
    app = AIDesktopChat()
    app.run()
    
    return True


if __name__ == "__main__":
    __init__()
    main()