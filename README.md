# 🏥 Sistema de Gestión de Citas Médicas

Un sistema integral de gestión de citas médicas diseñado para optimizar la administración hospitalaria, facilitando la interacción entre pacientes, médicos y personal administrativo a través de una interfaz web intuitiva.

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Documentación Técnica](#-documentación-técnica)
- [Contribución](#-contribución)
- [Issues Conocidos](#-issues-conocidos)
- [Roadmap](#-roadmap)

## ✨ Características Principales

### 👥 Gestión de Pacientes
- **Registro de pacientes**: Agregar nuevos pacientes al sistema
- **Búsqueda avanzada**: Localizar pacientes por número de identificación
- **Perfil completo**: Información detallada incluyendo datos de contacto

### 👨‍⚕️ Gestión de Médicos
- **Directorio médico**: Registro completo de médicos por especialidad
- **Agenda personalizada**: Cada médico tiene su propia agenda de citas
- **Sistema de calificaciones**: Evaluación de desempeño basada en feedback de pacientes

### 📅 Sistema de Citas
- **Agendamiento inteligente**: Verificación automática de disponibilidad
- **Citas de urgencia**: Manejo prioritario para emergencias médicas
- **Intervalos estructurados**: Citas programadas en bloques de 20 minutos (00, 20, 40)
- **Reprogramación flexible**: Capacidad de modificar o cancelar citas existentes

### 🔔 Sistema de Notificaciones
- **Recordatorios automáticos**: Notificaciones 2 días antes de la cita
- **Múltiples canales**: Correo electrónico, SMS y WhatsApp
- **Confirmaciones**: Validación de citas programadas

### ⭐ Feedback y Calificaciones
- **Evaluación post-cita**: Sistema de calificación de 0 a 5 estrellas
- **Comentarios detallados**: Feedback cualitativo de los pacientes
- **Rankings médicos**: Visualización de médicos mejor calificados

### 📊 Reportes y Analytics
- **Reportes de demanda**: Análisis de especialidades más solicitadas
- **Tendencias temporales**: Patrones de agendamiento a lo largo del tiempo
- **Análisis de ausentismo**: Métricas de eficiencia del sistema
- **Exportación**: Generación de reportes en formato Excel

## 🏗️ Arquitectura del Sistema

### Tecnologías Utilizadas
- **Backend**: Python 3.x
- **Framework Web**: Flask
- **Interfaz de Terminal**: Rich (para modo consola)
- **Datos**: CSV y JSON para persistencia
- **Frontend**: HTML templates con Jinja2

### Componentes Principales
```
Sistema de Gestión de Citas
├── Módulo de Pacientes
├── Módulo de Médicos  
├── Módulo de Agenda
├── Sistema de Notificaciones
├── Sistema de Feedback
└── Generador de Reportes
```

## 🚀 Instalación

### Prerrequisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd sistema-gestion-citas-medicas
   ```

2. **Crear entorno virtual** (recomendado)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar estructura de datos**
   Asegúrese de que existan los siguientes archivos en el directorio `data/`:
   - `pacientes.csv`
   - `medicos.json`
   - `citas.csv`

## 💻 Uso

### Ejecutar la Aplicación Web

```bash
python app/main.py
```

La aplicación estará disponible en `http://localhost:5000`

### Funcionalidades Disponibles

#### 📋 Menú Principal
- **Pacientes**: Agregar, buscar, listar pacientes y consultar sus citas
- **Médicos**: Gestionar directorio médico y consultar agendas
- **Citas**: Agendar, consultar y gestionar citas médicas
- **Feedback**: Sistema de calificaciones y comentarios
- **Reportes**: Análisis y métricas del sistema

#### 🔄 Flujo de Trabajo Típico

1. **Registrar un paciente**
   - Acceder a "Agregar Paciente"
   - Completar información: ID, nombre, celular, correo

2. **Agendar una cita**
   - Seleccionar "Agendar Cita"
   - Elegir paciente, especialidad y médico
   - Definir fecha/hora (intervalos de 20 min)
   - Marcar si es urgente

3. **Consultar agenda médica**
   - Usar "Citas del Médico"
   - Ingresar identificación del médico
   - Visualizar todas las citas programadas

4. **Evaluar atención**
   - Acceder a "Feedback"
   - Seleccionar cita realizada
   - Calificar del 0 al 5 y agregar comentarios

## 📁 Estructura del Proyecto

```
sistema-gestion-citas-medicas/
├── app/
│   ├── main.py              # Aplicación Flask principal
│   ├── hospital.py          # Clase principal del sistema
│   ├── agenda.py            # Gestión de citas y horarios
│   ├── paciente.py          # Modelo de paciente
│   ├── medico.py            # Modelo de médico
│   ├── cita.py              # Modelo de cita
│   ├── cita_urgente.py      # Modelo de cita urgente
│   ├── persona.py           # Clase base para personas
│   ├── notificacion*.py     # Sistema de notificaciones
│   ├── templates/           # Templates HTML
│   └── static/              # Archivos estáticos (CSS, JS)
├── data/
│   ├── pacientes.csv        # Base de datos de pacientes
│   ├── medicos.json         # Base de datos de médicos
│   └── citas.csv            # Registro de citas
├── docs/
│   ├── Listado_de_Requerimientos.md
│   ├── Issues.md
│   └── Diagrama_de_Clases.pdf
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

## 📚 Documentación Técnica

### Modelos de Datos

#### Paciente
```python
class Paciente:
    - identificacion: str
    - nombre: str
    - celular: str
    - correo: str
```

#### Médico
```python
class Medico:
    - identificacion: str
    - nombre: str
    - celular: str
    - especialidad: str
    - calificaciones: list
```

#### Cita
```python
class Cita:
    - paciente: Paciente
    - medico: Medico
    - fecha_hora: datetime
    - urgente: bool
    - feedback: dict
```

### API Endpoints (Flask)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Página principal |
| `/agregar_paciente` | GET/POST | Formulario de registro de pacientes |
| `/agendar_cita` | GET/POST | Sistema de agendamiento |
| `/citas_medico` | GET/POST | Consulta de agenda médica |
| `/feedback` | GET/POST | Sistema de calificaciones |
| `/ver_calificacion` | GET | Rankings de médicos |

## 🤝 Contribución

### Guías de Desarrollo

1. **Fork del repositorio**
2. **Crear rama de feature** (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit de cambios** (`git commit -am 'Agregar nueva funcionalidad'`)
4. **Push a la rama** (`git push origin feature/nueva-funcionalidad`)
5. **Crear Pull Request**

### Estándares de Código
- Seguir PEP 8 para estilo de Python
- Documentar funciones y clases
- Incluir tests para nuevas funcionalidades
- Mantener compatibilidad con Python 3.7+

## ⚠️ Issues Conocidos

Consultar `docs/Issues.md` para una lista detallada de problemas conocidos y limitaciones actuales:

- **Validaciones de horario**: Necesidad de mejorar validaciones de intervalos de tiempo
- **Gestión de agenda**: Considerar implementar agenda por médico para mejor rendimiento
- **Sistema de calificaciones**: Prevenir calificaciones duplicadas
- **Interfaz de usuario**: Mejorar experiencia de usuario en selección de especialidades
- **Documentación**: Aumentar comentarios en código y documentación técnica

## 🗺️ Roadmap

### Versión 2.0 (Próximamente)
- [ ] **Base de datos relacional**: Migración de CSV/JSON a PostgreSQL/MySQL
- [ ] **API RESTful**: Implementación de API completa
- [ ] **Autenticación**: Sistema de login para pacientes y médicos
- [ ] **Dashboard administrativo**: Panel de control para administradores
- [ ] **Notificaciones en tiempo real**: WebSockets para notificaciones instantáneas

### Versión 2.1
- [ ] **App móvil**: Aplicación nativa para iOS y Android
- [ ] **Integración con calendarios**: Sincronización con Google Calendar/Outlook
- [ ] **Reportes avanzados**: Dashboards interactivos con gráficos
- [ ] **Telemedicina**: Integración para consultas virtuales

### Versión 3.0
- [ ] **IA y Machine Learning**: Predicción de no-shows y optimización de horarios
- [ ] **Multi-idioma**: Soporte para múltiples idiomas
- [ ] **Multi-tenancy**: Soporte para múltiples hospitales/clínicas

---

## 📞 Soporte

Para reportar bugs, solicitar features o hacer preguntas técnicas, por favor:

1. Revisar los [issues existentes](docs/Issues.md)
2. Crear un nuevo issue describiendo el problema detalladamente
3. Incluir pasos para reproducir el problema
4. Especificar versión de Python y sistema operativo

## 📄 Licencia

Este proyecto está bajo desarrollo académico. Consultar con los autores para términos de uso y distribución.

---

**Desarrollado con ❤️ para mejorar la gestión hospitalaria**
