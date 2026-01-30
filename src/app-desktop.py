
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
# IA y BÚSQUEDA SEMÁNTICA
# ================================
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json
import re

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
        
        # Inicializar sistema de IA semántica
        print("🤖 Cargando modelo de IA...")
        self.embedding_model = None
        self.cisco_embeddings = None
        self.cisco_texts = []
        self.load_semantic_search_system()
        
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
            text="AI Cisco ASA 9.14 Chatbox", 
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
        self.response_text.insert("1.0", "Aquí aparecerá la respuesta de la IA Cisco ASA...")
        
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
        status_text = "Estado: ✅ IA Cisco ASA cargada y lista" if self.embedding_model else "Estado: ⚠️ IA no disponible"
        self.status_label = ctk.CTkLabel(
            main_frame, 
            text=status_text,
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
    
    def load_semantic_search_system(self):
        """Cargar sistema de búsqueda semántica con embeddings"""
        try:
            # Cargar modelo de embeddings ligero
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Cargar base de conocimiento Cisco
            knowledge_path = os.path.join("models", "cisco_knowledge_base.json")
            if os.path.exists(knowledge_path):
                with open(knowledge_path, 'r', encoding='utf-8') as f:
                    cisco_data = json.load(f)
                
                # Preparar textos para embeddings
                self.cisco_texts = []
                self.cisco_metadata = []
                
                # Filtrar y agregar comandos útiles
                for cmd in cisco_data.get('commands', []):
                    cmd_text = cmd.get('command', '').strip()
                    if (len(cmd_text) > 10 and len(cmd_text) < 200 and 
                        any(keyword in cmd_text.lower() for keyword in [
                            'show', 'configure', 'interface', 'router', 'access-list',
                            'crypto', 'nat', 'route', 'object', 'policy'
                        ])):
                        self.cisco_texts.append(cmd_text)
                        self.cisco_metadata.append({
                            'type': 'command',
                            'content': cmd_text,
                            'section': cmd.get('section', ''),
                            'line': cmd.get('line', 0)
                        })
                
                # Agregar configuraciones
                for config in cisco_data.get('configurations', []):
                    config_text = config.get('config', '').strip()
                    if len(config_text) > 10 and len(config_text) < 500:
                        self.cisco_texts.append(config_text)
                        self.cisco_metadata.append({
                            'type': 'configuration',
                            'content': config_text,
                            'section': config.get('section', ''),
                            'line': config.get('line', 0)
                        })
                
                # Crear embeddings si tenemos textos
                if self.cisco_texts:
                    print(f"📊 Creando embeddings para {len(self.cisco_texts)} elementos...")
                    self.cisco_embeddings = self.embedding_model.encode(self.cisco_texts)
                    print("✅ Sistema de IA semántica cargado")
                else:
                    print("⚠️ No se encontraron textos válidos para embeddings")
            else:
                print("⚠️ Base de conocimiento no encontrada. Ejecuta el entrenamiento primero.")
                
        except Exception as e:
            print(f"❌ Error cargando sistema de IA: {e}")
            self.embedding_model = None
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Realizar búsqueda semántica en la base de conocimiento"""
        if not self.embedding_model or not self.cisco_embeddings:
            return []
        
        try:
            # Crear embedding para la consulta
            query_embedding = self.embedding_model.encode([query])
            
            # Calcular similitud coseno
            similarities = cosine_similarity(query_embedding, self.cisco_embeddings)[0]
            
            # Obtener los top_k más similares
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.3:  # Umbral mínimo de similitud
                    result = self.cisco_metadata[idx].copy()
                    result['similarity'] = float(similarities[idx])
                    results.append(result)
            
            return results
        except Exception as e:
            print(f"Error en búsqueda semántica: {e}")
            return []
    
    def get_ai_response(self, prompt):
        """Obtener respuesta de la IA usando búsqueda semántica y base de conocimiento Cisco"""
        import time
        
        # Buscar información relevante usando IA semántica
        relevant_results = self.semantic_search(prompt, top_k=8)
        
        # Detectar si es una solicitud de información detallada
        detail_match = re.match(r'^(\d+)$', prompt.strip())
        if detail_match:
            return self.get_detailed_info(detail_match.group(1))
        
        # Detectar patrones como "más info punto 4" o "info 4"
        info_match = re.search(r'(?:más?\s+info|info|detalle).*?(\d+)', prompt.lower())
        if info_match:
            return self.get_detailed_info(info_match.group(1))
        
        # Si no hay sistema de IA disponible, usar método básico
        if not self.embedding_model:
            return self._get_basic_response(prompt)
        
        # Usar IA semántica para generar respuesta
        return self._generate_ai_response(prompt, relevant_results)
    
    def _get_basic_response(self, prompt: str) -> str:
        """Respuesta básica cuando no hay IA disponible"""
        return f"""⚠️ **Sistema de IA No Disponible**

❌ El sistema de inteligencia artificial no está cargado.

🔧 **Para activar la IA:**
1. Instala las dependencias: `pip install sentence-transformers scikit-learn`
2. Verifica que el archivo `models/cisco_knowledge_base.json` exista
3. Reinicia la aplicación

💡 **Consulta actual:** {prompt}

📋 Mientras tanto, puedes hacer consultas básicas sobre configuración Cisco."""
    
    def _generate_ai_response(self, prompt: str, relevant_results: List[Dict]) -> str:
        """Generar respuesta usando IA y resultados semánticos"""
        prompt_lower = prompt.lower()
        response_parts = []
        
        # Respuesta inteligente basada en contenido encontrado
        if relevant_results:
            # Encabezado genérico - que la IA determine el tema por el contenido
            response_parts.append("🤖 **IA Cisco ASA 9.14**")
            response_parts.append("Información extraída del manual oficial:")
            response_parts.append("")
            
            # Mostrar solo los resultados más relevantes
            high_relevance = [r for r in relevant_results if r['similarity'] > 0.5]
            
            if high_relevance:
                for i, result in enumerate(high_relevance[:4], 1):
                    similarity_percent = int(result['similarity'] * 100)
                    content = result['content'].strip()
                    
                    if result['type'] == 'command':
                        # Limpiar y formatear comandos
                        if len(content) > 80:
                            content = content[:77] + "..."
                        response_parts.append(f"**{i}. Comando** ({similarity_percent}% relevancia)")
                        response_parts.append(f"```")
                        response_parts.append(content)
                        response_parts.append("```")
                    else:
                        # Formatear configuraciones
                        if len(content) > 120:
                            content = content[:117] + "..."
                        response_parts.append(f"**{i}. Configuración** ({similarity_percent}% relevancia)")
                        response_parts.append(f"📝 {content}")
                    response_parts.append("")
                
                # Agregar solo un resumen breve
                response_parts.append("💡 **Resumen IA:**")
                command_count = sum(1 for r in high_relevance if r['type'] == 'command')
                config_count = sum(1 for r in high_relevance if r['type'] == 'configuration')
                
                if command_count > config_count:
                    response_parts.append(f"Encontré principalmente comandos de verificación y diagnóstico.")
                else:
                    response_parts.append(f"Encontré principalmente pasos de configuración.")
                
                response_parts.append(f"Total: {len(high_relevance)} elementos relevantes del manual oficial.")
            else:
                # Mostrar resultados de mediana relevancia si no hay alta
                medium_results = [r for r in relevant_results if r['similarity'] > 0.3][:3]
                if medium_results:
                    response_parts.append("📋 **Información relacionada encontrada:**")
                    for i, result in enumerate(medium_results, 1):
                        content = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
                        similarity_percent = int(result['similarity'] * 100)
                        response_parts.append(f"{i}. {content} ({similarity_percent}%)")
                    response_parts.append("")
                    response_parts.append("💡 La información tiene relevancia moderada. Intenta ser más específico.")
                else:
                    response_parts.append("❌ No encontré información específica en el manual.")
                    response_parts.append("💡 Intenta usar términos más técnicos como 'crypto map', 'isakmp', 'ipsec'.")
            
        else:
            # Respuesta cuando no hay resultados específicos - SIN contenido hardcodeado
            response_parts.append("🤖 **IA Cisco - Sin coincidencias en el manual**")
            response_parts.append(f"La IA no encontró información específica para: '{prompt}' en el manual ASA 9.14")
            response_parts.append("")
            response_parts.append("💡 **Intenta reformular con términos más técnicos del manual Cisco**")
            response_parts.append("📚 La respuesta se basa únicamente en el contenido oficial extraído del manual.")
        
        return "\n".join(response_parts)

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