# Ejercicio 3 - Visualizador de Bases de Datos en Aiven (Streamlit + MySQL)

## Explicación del Proyecto
Este proyecto consiste en el desarrollo de una aplicación web interactiva en Python que actúa como un **VISUALIZADOR DE BASE DE DATOS**. La aplicación simula el flujo completo de un entorno real de producción dividiéndose en tres componentes esenciales:
1. **Base de Datos (Almacenamiento):** Servidor gestionado MySQL alojado en la nube a través de la plataforma **Aiven**.
2. **Backend (Lógica en Python):** Funciones de conexión estructuradas, manejo de excepciones de red y control de estado de sesión.
3. **Frontend (Interfaz de Usuario):** Interfaz web dinámica con **Streamlit**.

La herramienta nos permite verificar de manera segura el estado de las tablas de datos, auditar métricas críticas (conteo de registros y campos), previsualizar el contenido en la nube en tiempo real y generar representaciones gráficas interactivas automatizadas de cualquier columna numérica para análisis rápidos frente a incidentes.

---

## Librerías Utilizadas: ¿Qué hacen y por qué se usan?

Para el correcto funcionamiento de esta herramienta se han seleccionado librerías específicas que garantizan eficiencia, seguridad en la nube y una experiencia de usuario fluida:

### 1. `streamlit`
* **¿Qué hace?:** Es un framework de código abierto orientado a la creación rápida de aplicaciones web de datos y paneles de control directamente desde scripts de Python puro, sin necesidad de maquetar con HTML, CSS o JavaScript.
* **¿Por qué se usa?:** Nos ofrece un despliegue rápido de nuestro proyecto. Además, proporciona componentes reactivos de alto nivel como paneles laterales (`st.sidebar`), menús de selección (`st.selectbox`), paneles de métricas (`st.metric`), contenedores de datos (`st.dataframe`) e integraciones directas con gráficos, permitiendo que la interacción del usuario actualice la pantalla de forma dinámica sin recargar completamente la página gracias al control que nos ofrece `st.session_state`.

### 2. `pymysql`
* **¿Qué hace?:** Es un conector nativo de Python para comunicarse con servidores de bases de datos MySQL y MariaDB. Permite conectarnos a SQL y manipular las bases de datos.
* **¿Por qué se usa?:** Es una librería crítica para interactuar con la base de datos de Aiven. Su uso es clave debido a su total compatibilidad con conexiones cifradas TLS/SSL mediante el parámetro `ssl={'ssl': {}}`, lo cual nos permite conectarnos a plataformas Cloud actuales (como Aiven), que permiten el tráfico y validen sockets desde redes externas de manera segura.

### 3. `pandas`
* **¿Qué hace?:** Es la librería líder en Python para manipulación, estructuración y análisis de datos a gran escala a través de su estructura principal: el *DataFrame*.
* **¿Por qué se usa?:** Se utiliza en conjunto con PyMySQL a través de la función `pd.read_sql_query()`. Esto permite transformar los datos binarios en formato tabla estructurada. Facilita enormemente el cálculo inmediato de estadísticas (como el conteo de filas con `len()` y columnas con `.columns`) y su renderizado directo en la interfaz sin necesidad de iterar manualmente sobre colecciones de tuplas.

---

## Instrucciones de Ejecución

Estas son las instrucciones para desplegar la aplicación en tu entorno:

### 1. Requisitos Previos
Tener instalado Python (versión 3.8 o superior) en tu sistema operativo (compatible con Windows, Linux o macOS).

### 2. Instalación de Dependencias
Instalar las tres librerías requeridas utilizando el gestor de paquetes de Python (`pip`). Una vez hecho esto, ejecutar la siguiente instrucción en la terminal:

```bash
pip install streamlit pymysql pandas