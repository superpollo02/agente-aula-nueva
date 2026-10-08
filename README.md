# 🎓 Agente Kit Aula Nueva (EducAI)

Este repositorio contiene una arquitectura Multi-Agente diseñada para automatizar la creación de la estructura instruccional de aulas virtuales en Moodle bajo la estricta metodología **Kit Aula Nueva**.

En lugar de delegar el trabajo a un solo agente de IA propenso a errores u omisiones, este proyecto implementa una **cadena de montaje (pipeline)** compuesta por 3 especialistas que interactúan de forma secuencial.

---

## 👥 Los 3 Agentes (Secuencia de Trabajo)

El flujo de trabajo está diseñado con un control de calidad cruzado:

### `01_analista_academico` (Filtro inicial)
- **Función:** Analiza el programa analítico provisto.
- **Actitud:** Estricto y burocrático.
- **Acción:** Verifica la viabilidad (carga horaria) y exige que no falte información como la bibliografía. Si el input está correcto, fija la audiencia y aprueba el pase a la fase de diseño.

### `02_disenador_instruccional` (Cerebro Pedagógico)
- **Función:** Es el núcleo creativo de la metodología Kit Aula Nueva.
- **Actitud:** Enfocado en la andragogía (aprendizaje del adulto) y en reducir la carga cognitiva.
- **Acción:** Ejecuta 3 tareas en orden: 
  1. Diseña "La Clase" (Videos cápsula y PDF).
  2. Diseña "La Lectura" (Glosarios y FAQs basados en la clase).
  3. Diseña "La Práctica" (Trivias y recursos gamificados SCORM).

### `03_auditor_tecnico_moodle` (Control de Calidad QA)
- **Función:** Ensamblaje final e inspección técnica.
- **Actitud:** Técnico obsesivo informático. No opina sobre pedagogía.
- **Acción:** Recibe el trabajo del diseñador y se asegura estrictamente de que se apliquen las reglas de Moodle: candados de examen final, atributos `target="_blank"` y agrupamiento de PDFs en carpetas temáticas. Ensambla el Markdown final.

---

## ⚙️ Características Técnicas

- **Sin frameworks pesados:** No utiliza CrewAI ni AutoGen, evadiendo problemas de dependencias con numpy o incompatibilidades en Windows. Se usa Python puro y la librería liviana `google-generativeai`.
- **Integración YAML:** Arquitectura ordenada donde las configuraciones del modelo, los perfiles de agentes (`config/agents.yaml`) y las instrucciones paso a paso (`config/tasks.yaml`) están separadas del código ejecutable.
- **Context Passing:** Cada agente hereda el contexto de lo que hizo el agente anterior, garantizando coherencia absoluta entre los videos propuestos y los glosarios resultantes.

---

## 🚀 Cómo instalar y activarlo

### 1. Clonar el repositorio
```bash
git clone https://github.com/superpollo02/agente-aula-nueva.git
cd agente-aula-nueva
```

### 2. Preparar el entorno (Opcional pero recomendado)
```bash
python -m venv venv
# En Windows:
.\venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
```

### 3. Instalar librerías ligeras
Solo necesitas la librería de Google y PyYAML para leer las configuraciones.
```bash
pip install google-generativeai pyyaml
```

### 4. Configurar API Key
Necesitás una API Key gratuita de Gemini (obtenible en Google AI Studio).

**En PowerShell (Windows):**
```powershell
$env:GEMINI_API_KEY="TU_CLAVE_AQUI"
```
**En Bash (Mac/Linux):**
```bash
export GEMINI_API_KEY="TU_CLAVE_AQUI"
```

### 5. Ejecutar
Abrí el archivo `main.py` y modificá la variable `programa_ejemplo` para insertar el programa académico analítico real de tu materia.

Luego, ejecutá:
```bash
python main.py
```

En la consola verás paso a paso qué agente está trabajando. Al finalizar, obtendrás el archivo `propuesta_aula_auditada.md` listo para subir a tu plataforma o presentar a tu equipo.
