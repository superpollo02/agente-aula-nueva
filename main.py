"""
Kit Aula Nueva (EducAI) - Orquestador Multi-Agente
Automatiza la creación de aulas virtuales en Moodle bajo la metodología Kit Aula Nueva.
"""

import os
import sys
import argparse
import time
from pathlib import Path
import yaml

# Cargar variables de entorno desde .env si existe
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Asegurar codificación UTF-8 en consola de Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Detección del cliente de Google Gemini (moderno google-genai con fallback a google-generativeai)
USE_MODERN_SDK = False
try:
    from google import genai
    from google.genai import types
    USE_MODERN_SDK = True
except ImportError:
    try:
        import google.generativeai as legacy_genai
        USE_MODERN_SDK = False
    except ImportError:
        pass


def load_yaml(file_path):
    """Carga un archivo YAML con codificación utf-8."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {file_path}")
    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


class AgenteRunner:
    """Ejecutor de agentes compatible con google-genai moderno y google-generativeai heredado."""

    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash", mock: bool = False):
        self.api_key = api_key
        self.model_name = model_name
        self.mock = mock
        self.client = None

        if not self.mock:
            if USE_MODERN_SDK:
                self.client = genai.Client(api_key=self.api_key)
            else:
                legacy_genai.configure(api_key=self.api_key)

    def ejecutar_tarea(self, nombre_tarea: str, tarea_config: dict, agente_config: dict, contexto_previo: str = "", verbose: bool = False) -> str:
        """Ejecuta una tarea asignada a un agente específico."""
        rol = agente_config.get("role", "Agente").strip()
        print(f"\n[{rol}] Ejecutando: {nombre_tarea}...")

        prompt = tarea_config["description"].replace("{contexto}", contexto_previo)
        prompt += f"\n\nOUTPUT ESPERADO:\n{tarea_config['expected_output']}"
        system_instruction = (
            f"Rol: {agente_config.get('role', '')}\n\n"
            f"Objetivo: {agente_config.get('goal', '')}\n\n"
            f"Contexto y Personalidad: {agente_config.get('backstory', '')}"
        )

        if self.mock:
            time.sleep(0.5)
            respuesta_texto = self._generar_mock(nombre_tarea, contexto_previo)
        else:
            if USE_MODERN_SDK:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config,
                )
                respuesta_texto = response.text
            else:
                modelo = legacy_genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=system_instruction,
                )
                response = modelo.generate_content(prompt)
                respuesta_texto = response.text

        if verbose:
            print(f"\n--- Output de [{nombre_tarea}] ---")
            print(respuesta_texto[:400] + ("..." if len(respuesta_texto) > 400 else ""))
            print("---------------------------------")

        return respuesta_texto

    def _generar_mock(self, nombre_tarea: str, contexto: str) -> str:
        """Genera respuestas simuladas realistas para pruebas sin consumir cuota de API."""
        if nombre_tarea == "analisis_y_planificacion":
            return (
                "### DICTAMEN DE PLANIFICACIÓN ACADÉMICA (Aprobado)\n\n"
                "- **Unidad 1:** Introducción a la Andragogía (10 horas) -> **Aprobada**.\n"
                "- **Unidad 2:** Diseño Moodle (15 horas) -> **Aprobada**.\n"
                "- **Audiencia fijada:** Docentes y profesionales de educación superior y formación continua.\n"
                "- **Recomendaciones:** Mantener la separación de unidades dada la especificidad técnica de Moodle.\n"
            )
        elif nombre_tarea == "diseno_clase_audiovisual":
            return (
                "### 1. La Clase\n\n"
                "#### Unidad 1: Introducción a la Andragogía\n"
                "- **Video-lección principal (25 min):** 'Fundamentos del Aprendizaje Adulto y Carga Cognitiva'.\n"
                "- **Short IA (2 min):** '3 claves para captar la atención del alumno adulto'.\n"
                "- **Diapositivas de apoyo:** Carpeta con PDF descargable de la presentación.\n\n"
                "#### Unidad 2: Diseño Moodle\n"
                "- **Video-lección principal (28 min):** 'Estructuración modular y recursos SCORM en Moodle'.\n"
                "- **Short IA (2 min):** 'Cómo evitar el abandono con foros activos'.\n"
                "- **Diapositivas de apoyo:** Guía paso a paso en PDF."
            )
        elif nombre_tarea == "diseno_lectura_teorica":
            return (
                "### 2. La Lectura\n\n"
                "#### Unidad 1: Introducción a la Andragogía\n"
                "- **Glosario terminológico:** Andragogía, Carga cognitiva extrínseca/intrínseca, Aprendizaje autodirigido.\n"
                "- **FAQ (20 preguntas clave):** Preguntas frecuentes sobre retención adulta y diseño instruccional.\n"
                "- **Infografía de síntesis:** Mapa conceptual de la teoría de Knowles (1984).\n"
                "- **Lecturas obligatorias:** PDFs organizados por temática.\n\n"
                "#### Unidad 2: Diseño Moodle\n"
                "- **Glosario:** SCORM, Rastreo de finalización, Agrupamiento, Restricciones de acceso.\n"
                "- **FAQ:** Resolución de problemas comunes en configuración de exámenes.\n"
                "- **Infografía:** Flujograma de finalización de curso.\n"
                "- **Lecturas:** Manual técnico oficial de Moodle 2024."
            )
        elif nombre_tarea == "diseno_practica_gamificada":
            return (
                "### 3. La Práctica\n\n"
                "#### Unidad 1: Introducción a la Andragogía\n"
                "- **Consigna orientadora:** Visualizar el video principal y resolver el caso práctico del estudiante desmotivado.\n"
                "- **Trivia SCORM (sin numeración rígida):** Reto contrarreloj de 5 minutos sobre principios andragógicos.\n"
                "- **Conecta Bloques:** Emparejamiento de conceptos del glosario con ejemplos de aula.\n"
                "- **Calificación:** 10 puntos con retroalimentación automática inmediata.\n\n"
                "#### Unidad 2: Diseño Moodle\n"
                "- **Consigna:** Configurar un aula demo aplicando los criterios de los videos.\n"
                "- **Trivia SCORM (sin numeración rígida):** Diagnóstico de errores de configuración.\n"
                "- **Examen final sumativo:** Cuestionario integrador con acceso condicionado (candado)."
            )
        elif nombre_tarea == "ensamblaje_y_auditoria":
            return (
                "# Propuesta de Aula Virtual - Kit Aula Nueva\n\n"
                "## Unidad 1: Introducción a la Andragogía\n\n"
                "**1. La Clase**\n"
                "- Video-lección principal (25 min): <a href='https://moodle.ejemplo.edu/video1' target='_blank'>Fundamentos del Aprendizaje Adulto</a>\n"
                "- Video resumen: Short IA (2 min) resumen conceptual.\n"
                "- Diapositivas de apoyo: Disponibles en la carpeta temática de recursos.\n\n"
                "**2. La Lectura**\n"
                "- Glosario terminológico de andragogía y carga cognitiva.\n"
                "- FAQ de 20 preguntas frecuentes.\n"
                "- Infografía de síntesis descargable.\n"
                "- Carpeta temática: 'Lecturas Obligatorias - Unidad 1' con bibliografía de Knowles (1984).\n\n"
                "**3. La Práctica**\n"
                "- Consigna orientadora referenciando la video-lección principal.\n"
                "- Trivia SCORM interactiva sin numeración rígida.\n"
                "- Dinámica 'Conecta Bloques' para afianzar conceptos clave.\n\n"
                "✓ Checklist técnico verificado: Enlaces con target='_blank', PDFs en carpetas temáticas, trivias sin numeración rígida.\n\n"
                "---\n\n"
                "## Unidad 2: Diseño Moodle\n\n"
                "**1. La Clase**\n"
                "- Video-lección principal (28 min): <a href='https://moodle.ejemplo.edu/video2' target='_blank'>Estructura y SCORM</a>\n"
                "- Video resumen: Short IA (2 min).\n"
                "- Diapositivas en carpeta temática.\n\n"
                "**2. La Lectura**\n"
                "- Glosario de Moodle y estándares SCORM.\n"
                "- FAQ técnica.\n"
                "- Carpeta temática: 'Documentación Oficial Moodle 2024'.\n\n"
                "**3. La Práctica**\n"
                "- Taller de configuración práctica.\n"
                "- Trivia SCORM sin numeración rígida.\n"
                "- Examen final sumativo con acceso condicionado (candado al completar Unidad 1 y 2).\n\n"
                "✓ Checklist técnico verificado: Enlace con target='_blank', examen final con candado de acceso condicionado, PDFs agrupados en carpetas temáticas.\n"
            )
        return f"[Resultado simulado para {nombre_tarea}]"


PROGRAMA_DEFAULT = """Unidad 1: Introducción a la Andragogía
Carga horaria: 10 horas
Contenidos mínimos: Teoría del aprendizaje adulto, Carga cognitiva.
Bibliografía obligatoria: Knowles (1984) - El aprendiz adulto.

Unidad 2: Diseño Moodle
Carga horaria: 15 horas
Contenidos mínimos: Configuración de cuestionarios SCORM, Foros.
Bibliografía obligatoria: Documentación oficial Moodle (2024).
"""


def parse_arguments():
    """Configura los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Agente Kit Aula Nueva (EducAI) - Automatización Multi-Agente para Moodle"
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        default=None,
        help="Ruta al archivo de texto o markdown con el programa analítico. Si no se indica, usa el de ejemplo."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="propuesta_aula_auditada.md",
        help="Nombre del archivo Markdown de salida (por defecto: propuesta_aula_auditada.md)."
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        default=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
        help="Modelo de Google Gemini a utilizar (por defecto: gemini-2.5-flash o GEMINI_MODEL en .env)."
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Modo simulación (Dry-Run): ejecuta todo el flujo con respuestas simuladas sin requerir API key."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Muestra detalles extendidos de salida en cada etapa del pipeline."
    )
    return parser.parse_args()


def run():
    args = parse_arguments()

    print("=" * 68)
    print("🎓 KIT AULA NUEVA (EducAI) - PIPELINE MULTI-AGENTE")
    print("=" * 68)

    # Verificación de credenciales
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key and not args.mock:
        print("\n[!] ERROR: No se encontró la variable GEMINI_API_KEY.")
        print("Para configurarla:")
        print("  1. Creá un archivo '.env' en la raíz con: GEMINI_API_KEY=tu_clave")
        print("  2. O definí la variable en tu terminal: $env:GEMINI_API_KEY=\"tu_clave\"")
        print("  3. O ejecutá en modo simulación para probar sin API key: python main.py --mock\n")
        sys.exit(1)

    # Cargar configuraciones de agentes y tareas
    try:
        agents = load_yaml("config/agents.yaml")
        tasks = load_yaml("config/tasks.yaml")
    except Exception as e:
        print(f"\n[!] Error al cargar la configuración YAML: {e}")
        sys.exit(1)

    # Cargar programa analítico
    if args.input:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"\n[!] Error: El archivo de entrada '{args.input}' no existe.")
            sys.exit(1)
        with open(input_path, "r", encoding="utf-8") as f:
            programa_academico = f.read()
        print(f"[*] Programa cargado desde: {args.input}")
    else:
        programa_academico = PROGRAMA_DEFAULT
        print("[*] Usando programa académico de ejemplo.")

    print(f"[*] Modelo: {args.model} {'(MODO MOCK)' if args.mock else ''}")
    print(f"[*] SDK: {'google-genai (v2)' if USE_MODERN_SDK else 'google-generativeai (legacy)'}")

    # Inicializar orquestador
    runner = AgenteRunner(api_key=api_key or "", model_name=args.model, mock=args.mock)

    inicio = time.time()

    # Flujo secuencial (Pipeline)
    # Tarea 1: Analista (Agente 01)
    res_t1 = runner.ejecutar_tarea(
        "analisis_y_planificacion",
        tasks["analisis_y_planificacion"],
        agents["01_analista_academico"],
        programa_academico,
        verbose=args.verbose
    )

    # Tarea 2: Diseñador - Clase (Agente 02)
    res_t2 = runner.ejecutar_tarea(
        "diseno_clase_audiovisual",
        tasks["diseno_clase_audiovisual"],
        agents["02_disenador_instruccional"],
        res_t1,
        verbose=args.verbose
    )

    # Tarea 3: Diseñador - Lectura (Agente 02)
    res_t3 = runner.ejecutar_tarea(
        "diseno_lectura_teorica",
        tasks["diseno_lectura_teorica"],
        agents["02_disenador_instruccional"],
        res_t2,
        verbose=args.verbose
    )

    # Tarea 4: Diseñador - Práctica (Agente 02)
    contexto_t4 = f"Clases:\n{res_t2}\n\nLecturas:\n{res_t3}"
    res_t4 = runner.ejecutar_tarea(
        "diseno_practica_gamificada",
        tasks["diseno_practica_gamificada"],
        agents["02_disenador_instruccional"],
        contexto_t4,
        verbose=args.verbose
    )

    # Tarea 5: Auditor Técnico (Agente 03)
    contexto_final = f"{res_t2}\n\n{res_t3}\n\n{res_t4}"
    res_t5 = runner.ejecutar_tarea(
        "ensamblaje_y_auditoria",
        tasks["ensamblaje_y_auditoria"],
        agents["03_auditor_tecnico_moodle"],
        contexto_final,
        verbose=args.verbose
    )

    # Guardar archivo final
    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(res_t5)

    duracion = time.time() - inicio
    print("\n" + "=" * 68)
    print("✨ ¡PROCESO FINALIZADO CON ÉXITO!")
    print(f"⏱️ Tiempo total: {duracion:.2f} segundos")
    print(f"📄 Archivo generado: {output_path.resolve()}")
    print("=" * 68)


if __name__ == "__main__":
    run()
