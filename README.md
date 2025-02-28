# Monitor TXT

Este es un script en Python para monitorear cambios en archivos de texto dentro de una carpeta específica y enviar su contenido a Open WebUI para recibir respuestas automatizadas de un modelo de IA.

## 📌 Requisitos previos

Antes de ejecutar el script, asegúrate de tener instalados los siguientes programas y herramientas:

1. **Python 3.x** instalado en tu sistema.
2. **Open WebUI** en ejecución en `http://localhost:9090`
3. **Ollama** corriendo con modelos instalados.
4. **Dependencias de Python**, instaladas con:
   ```bash
   pip install -r requirements.txt
   ```
5. **Configurar tu API Key en un archivo `.env`**:
   - Crea un archivo llamado `.env` en la carpeta del proyecto.
   - Agrega tu API Key de Open WebUI:
     ```
     API_KEY=tu_api_key_aqui
     ```

## 🚀 Instalación y uso

1. Clona este repositorio y entra en la carpeta del proyecto:
   ```bash
   git clone https://github.com/tuusuario/monitor-txt.git
   cd monitor-txt
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta Open WebUI en el puerto 9090:
   ```bash
   open-webui serve --port 9090
   ```

4. Accede a Open WebUI desde tu navegador en:
   ```
   http://localhost:9090/auth
   ```

5. Asegúrate de tener modelos en Ollama:
   ```bash
   ollama run codellama:13b
   ```
   o
   ```bash
   ollama run deepseek-coder:latest
   ```

6. Ejecuta el script en Python:
   ```bash
   python main.py
   ```

7. Selecciona la carpeta que deseas monitorear y comienza a recibir respuestas del modelo en la interfaz gráfica.

## 📚 Funcionalidades

- Monitorea en tiempo real archivos `.txt` dentro de una carpeta.
- Detecta cambios en archivos existentes y muestra sus modificaciones.
- Envía el contenido a Open WebUI y recibe respuestas de un modelo de IA.
- Permite enviar prompts manuales al modelo seleccionado.
- Soporta múltiples modelos y permite cambiar entre ellos desde la interfaz.

## 🔧 Archivos importantes

- `main.py`: Script principal del programa.
- `.env`: Archivo de configuración con la API Key (no debe subirse a GitHub).
- `.gitignore`: Archivos que deben excluirse del repositorio.
- `requirements.txt`: Dependencias necesarias para ejecutar el programa.

## 🤖 Modelos soportados

Actualmente el script puede trabajar con los modelos disponibles en Ollama. Para listar los modelos instalados, usa:
   ```bash
   ollama list
   ```

## 🛠️ Contribuciones

Si quieres contribuir con mejoras, crea un **pull request** o abre un **issue** en GitHub.

## 📜 Licencia

Este proyecto está bajo la licencia MIT.

