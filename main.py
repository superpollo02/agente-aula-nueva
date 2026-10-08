import os
import yaml
import google.generativeai as genai

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def crear_modelo(agente_config):
    """Crea una instancia de Gemini configurada con el rol y personalidad del agente"""
    system_instruction = f"Rol: {agente_config['role']}\n\nObjetivo: {agente_config['goal']}\n\nContexto y Personalidad: {agente_config['backstory']}"
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction
    )

def ejecutar_tarea(nombre_tarea, tarea_config, agente_config, contexto_previo=""):
    """Ejecuta una tarea específica usando el agente asignado"""
    print(f"[{agente_config['role']}] Ejecutando: {nombre_tarea}...")
    
    modelo = crear_modelo(agente_config)
    prompt = tarea_config['description'].replace('{contexto}', contexto_previo)
    prompt += f"\n\nOUTPUT ESPERADO:\n{tarea_config['expected_output']}"
    
    respuesta = modelo.generate_content(prompt)
    return respuesta.text

def run():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Configura la variable de entorno GEMINI_API_KEY")
        return
    
    genai.configure(api_key=api_key)
    
    # Cargar configuraciones
    agents = load_yaml("config/agents.yaml")
    tasks = load_yaml("config/tasks.yaml")
    
    # Input inicial del usuario
    programa_ejemplo = '''
    Unidad 1: Introducción a la Andragogía
    Carga horaria: 10 horas
    Contenidos mínimos: Teoría del aprendizaje adulto, Carga cognitiva.
    Bibliografía obligatoria: Knowles (1984) - El aprendiz adulto.
    
    Unidad 2: Diseño Moodle
    Carga horaria: 15 horas
    Contenidos mínimos: Configuración de cuestionarios SCORM, Foros.
    Bibliografía obligatoria: Documentación oficial Moodle (2024).
    '''
    
    print("--- INICIANDO FLUJO DE TRABAJO MULTI-AGENTE (KIT AULA NUEVA) ---\n")
    
    # Flujo secuencial (Pipeline)
    # Tarea 1: Analista (Agente 01)
    resultado_t1 = ejecutar_tarea("analisis_y_planificacion", tasks["analisis_y_planificacion"], agents["01_analista_academico"], programa_ejemplo)
    
    # Tarea 2: Diseñador - Clase (Agente 02)
    resultado_t2 = ejecutar_tarea("diseno_clase_audiovisual", tasks["diseno_clase_audiovisual"], agents["02_disenador_instruccional"], resultado_t1)
    
    # Tarea 3: Diseñador - Lectura (Le pasamos la clase como contexto)
    resultado_t3 = ejecutar_tarea("diseno_lectura_teorica", tasks["diseno_lectura_teorica"], agents["02_disenador_instruccional"], resultado_t2)
    
    # Tarea 4: Diseñador - Práctica (Le pasamos lectura y clase)
    contexto_t4 = f"Clases:\n{resultado_t2}\n\nLecturas:\n{resultado_t3}"
    resultado_t4 = ejecutar_tarea("diseno_practica_gamificada", tasks["diseno_practica_gamificada"], agents["02_disenador_instruccional"], contexto_t4)
    
    # Tarea 5: Auditor Técnico (Agente 03)
    contexto_final = f"{resultado_t2}\n\n{resultado_t3}\n\n{resultado_t4}"
    resultado_t5 = ejecutar_tarea("ensamblaje_y_auditoria", tasks["ensamblaje_y_auditoria"], agents["03_auditor_tecnico_moodle"], contexto_final)
    
    # Guardar archivo final
    with open("propuesta_aula_auditada.md", "w", encoding="utf-8") as f:
        f.write(resultado_t5)
        
    print("\n--- ¡PROCESO FINALIZADO! ---")
    print("El archivo 'propuesta_aula_auditada.md' ha sido generado exitosamente.")

if __name__ == "__main__":
    run()
