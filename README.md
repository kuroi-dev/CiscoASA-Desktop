# AI Document Trainer - Cisco ASA

## Descripción

Sistema de asistencia para documentación Cisco ASA que permite consultar configuraciones, troubleshooting y administración de firewalls mediante una interfaz conversacional.

El sistema utiliza una base de conocimiento procesada a partir del manual Cisco ASA 9.14.

---

## Funcionalidades

### Consultas soportadas
- VPN Site-to-Site
- NAT (dinámico y estático)
- Firewall policies / ACLs
- Routing
- Interfaces

### Capacidades del sistema
- Respuestas paso a paso para configuraciones
- Explicaciones de comandos Cisco ASA
- Soporte para troubleshooting estructurado
- Navegación interactiva por consultas
- Base de conocimiento especializada

---

## Arquitectura del sistema
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
## Instalación

```bash
pip install -r requirements.txt
```

---

## Ejecución

```bash
python src/app-desktop.py
```

---

## Ejemplo de uso

Consulta:
configurar vpn

---

## Estado del proyecto

- Desktop App: Funcional
- Web App: En desarrollo
- API REST: Pendiente

---

## Autor

David Riquelme
