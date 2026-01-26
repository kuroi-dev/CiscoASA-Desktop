# AI Document Trainer - Consultor Cisco ASA

## Descripción
Sistema de inteligencia artificial especializado en documentación Cisco ASA que actúa como un **consultor experto conversacional**. Proporciona guías paso a paso detalladas para configuración, troubleshooting y administración de firewalls Cisco ASA.

### Características Principales
- **Especialización VPN**: Configuración detallada de túneles Site-to-Site
- **Firewall Expert**: Reglas de acceso y políticas de seguridad  
- **NAT Configurator**: Traducción de direcciones dinámicas y estáticas
- **Routing Guide**: Configuración de rutas estáticas y dinámicas
- **IA Conversacional**: Respuestas como un consultor humano experto
- **Interfaz Desktop**: Aplicación nativa con CustomTkinter

## Estado del Proyecto

### **COMPLETADO - Aplicación Desktop**
- Sistema de autenticación con PIN
- Procesamiento completo manual Cisco ASA 9.14 (1,408 páginas)
- Base de conocimiento con 9,660 comandos extraídos
- Interfaz conversacional tipo chatbot
- Navegación interactiva "más info punto X"
- Guías paso a paso para configuraciones

### **EN DESARROLLO - Aplicación Web** 
- Interfaz web con Flask/FastAPI
- API REST para consultas remotas
- Dashboard administrativo
- Multi-usuario y sesiones

## Arquitectura del Sistema

### **Hardware Objetivo**
- **GPU**: RTX 3070 (para procesamiento IA)
- **RAM**: 48GB (manejo de grandes documentos)  
- **CPU**: AMD Ryzen 5 7600X 6-Core

### **Estructura del Proyecto**
```
consulting/
├── src/                    # Aplicaciones
│   ├── app-desktop.py     # App desktop (FUNCIONAL)
│   └── app-web.py         # App web (EN DESARROLLO)
├── models/                # Autenticación y procesamiento
│   ├── authenticator_models.py
│   └── cisco_knowledge_base.json (3.8MB)
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## Funcionalidades Implementadas

### **IA Conversacional**
La IA responde como un **consultor Cisco experto** que te guía exactamente:
- **Qué botones presionar** en ASDM
- **Qué valores ingresar** en cada campo
- **Cómo navegar** entre pestañas y menús
- **Cómo verificar** que la configuración funciona

### **Aplicación Desktop**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python src/app-desktop.py
```
- **PIN**: 1234 (desarrollo)
- **Consultas soportadas**: VPN, NAT, Firewall, Routing, Interfaces
- **Navegación**: Escribe números para ver detalles específicos

### **Aplicación Web (En Desarrollo)**
```bash
# Próximamente
python src/app-web.py
```

## Ejemplos de Uso

### **Consulta**: "configurar vpn"
**Respuesta de la IA**:
```
Te ayudo a configurar tu VPN paso a paso:

PASO 1: Acceso a la Configuración
   → Ve al menú 'Configuration' > 'Site-to-Site VPN'

PASO 2: Configuración de Red Local  
   → En la casilla 'Local Network', ingresa: 192.168.1.0/24

PASO 3: Configuración de Red Remota
   → Casilla 'Remote IP': La IP pública del otro extremo
   → Ejemplo: 203.0.113.5
```

### **Navegación Interactiva**
```
Usuario: "3"
IA: "¡Aquí está toda la información del elemento 3!"
    [Información detallada del comando específico]
```

## Métricas del Sistema
- **Manual procesado**: Cisco ASA 9.14 (1,408 páginas)
- **Comandos extraídos**: 9,660 comandos únicos
- **Configuraciones**: 8,518 elementos  
- **Troubleshooting**: 511 elementos
- **Base de datos**: 3.8 MB
- **Tiempo de respuesta**: <2 segundos

## Roadmap

### **Fase 1**: Desktop App **COMPLETADA**
- [x] Interfaz desktop nativa
- [x] Sistema de autenticación  
- [x] IA conversacional especializada
- [x] Navegación interactiva

### **Fase 2**: Web App **EN DESARROLLO**
- [ ] API REST
- [ ] Interfaz web responsive
- [ ] Multi-usuario
- [ ] Dashboard administrativo

### **Fase 3**: Expansión **PLANIFICADA**
- [ ] Soporte para más dispositivos Cisco
- [ ] Integración con laboratorios virtuales
- [ ] Exportación de configuraciones
- [ ] Sistema de plantillas

---
**Proyecto desarrollado por David**  
*Iniciado: 26 de enero de 2026*  
*Estado: Aplicación Desktop Funcional | App Web en Desarrollo*