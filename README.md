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

## ⚙️ Características Técnicas y Mejoras

- **Nuevo SDK Oficial Google GenAI (`google-genai`):** Compatible con la API actual de Gemini (con fallback automático a `google-generativeai`).
- **Soporte para modelos modernos:** Configurado por defecto con `gemini-2.5-flash` (más rápido, preciso y económico).
- **Sin frameworks pesados:** No requiere CrewAI ni AutoGen, evitando problemas de dependencias pesadas y garantizando compatibilidad total en Windows, Mac y Linux.
- **Soporte para variables en `.env`:** Carga automática mediante `python-dotenv` para no tener que configurar variables de entorno en cada sesión de terminal.
- **CLI flexible:** Soporte para parámetros de consola (`--input`, `--output`, `--model`, `--mock`, `--verbose`).
- **Modo Simulación (`--mock`):** Permite ejecutar todo el pipeline con respuestas realistas de prueba sin consumir cuota ni requerir API key.
- **Integración YAML:** Arquitectura ordenada donde los perfiles de agentes (`config/agents.yaml`) y las instrucciones (`config/tasks.yaml`) están desacoplados del código ejecutable.
- **Compatibilidad UTF-8:** Soporte robusto de codificación para consolas Windows (PowerShell / CMD).

---

## 🚀 Cómo instalar y ejecutar

### 1. Clonar el repositorio
```bash
git clone https://github.com/superpollo02/agente-aula-nueva.git
cd agente-aula-nueva
```

### 2. Preparar el entorno virtual
```bash
python -m venv venv

# En Windows (PowerShell):
.\venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

### 3. Instalar librerías
```bash
pip install -r requirements.txt
```

### 4. Configurar tu API Key de Gemini
Obtené tu clave gratuita en [Google AI Studio](https://aistudio.google.com/).

Podés configurarla de dos formas:

**Opción A (Recomendada - Archivo `.env`):**
Copiá el archivo de ejemplo y colocá tu clave:
```bash
cp .env.example .env
```
Y editá `.env`:
```env
GEMINI_API_KEY=tu_clave_aqui
GEMINI_MODEL=gemini-2.5-flash
```

**Opción B (Variable de Entorno):**
- **PowerShell (Windows):** `$env:GEMINI_API_KEY="TU_CLAVE_AQUI"`
- **Bash (Mac/Linux):** `export GEMINI_API_KEY="TU_CLAVE_AQUI"`

---

## 💻 Modos de Ejecución

### Ejecución básica
Usa el programa analítico de ejemplo por defecto:
```bash
python main.py
```

### Usar tu propio programa académico desde un archivo
```bash
python main.py --input ejemplos/programa_ejemplo.txt
```

### Personalizar el archivo de salida
```bash
python main.py --input mi_materia.txt --output resultado_moodle.md
```

### Cambiar de modelo
```bash
python main.py --model gemini-2.5-pro
```

### Modo Simulación (Dry-Run / Sin API Key)
Probá todo el pipeline inmediatamente sin costo ni credenciales:
```bash
python main.py --mock --verbose
```

Al finalizar la ejecución, se generará el archivo `propuesta_aula_auditada.md` listo para ser implementado en tu plataforma Moodle.
