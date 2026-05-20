import streamlit as st
import pymysql
import pandas as pd

#La función establece la conexión con la base de datos MySQL en Aiven utilizando la librería PyMySQL.
def conectar_base_datos(host, port, user, password, database):
    #Nos conectamos a la base de datos utilizando los parámetros indicados manejando los posibles errores de conexión.
    try:
        conexion = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            ssl={'ssl': {}}, 
            connect_timeout=10
        )
        return conexion
    except pymysql.MySQLError as e:
        st.sidebar.error(f"❌ Error de conexión: {e}")
        return None

#Función que recupera la lista de tablas disponibles en la base de datos manejando los posibles errores.
def obtener_tablas(conexion):
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tablas = [tabla[0] for tabla in cursor.fetchall()]
        return tablas
    except pymysql.MySQLError as e:
        st.error(f"Error al listar las tablas: {e}")
        return []

#Función que consulta los registros de una tabla específica utilizando Pandas y PyMySQL manejando los posibles errores.
def consultar_tabla(conexion, nombre_tabla):
    try:
        query = f"SELECT * FROM `{nombre_tabla}`;" 
        df = pd.read_sql_query(query, conexion) 
        return df
    except Exception as e:
        st.error(f"Error al ejecutar la consulta en la tabla {nombre_tabla}: {e}")
        return None

# Configuración de la página web (título, icono y diseño).
st.set_page_config(
    page_title="Visualizador de bases de datos en Aiven",
    page_icon="🗂️",
    layout="wide"
)

# Título y Descripción informativa.
st.title("🗂️ VISUALIZADOR DE BASES DE DATOS EN AIVEN")
st.markdown("""
**Ejercicio 3 - VISUALIZACIÓN DE DATOS CON STREAMLIT**
Con esta interfaz se puede verificar el estado de la base de datos. 
""")

st.divider()

st.sidebar.header("Conexión a MySQL (Aiven)")
st.sidebar.markdown("Introduce los parámetros de tu servicio:")

# Parámetros de conexión a la base de datos MySQL en Aiven. Cuando el usuario termine de introducir los datos, podrá pulsar el botón para verificar la conexión.
db_host = st.sidebar.text_input("Host (URI)", value="mysql-164f68bc-guillermocuaresmautrerapj-5327.j.aivencloud.com")
db_port = st.sidebar.number_input("Puerto", value=11219)
db_user = st.sidebar.text_input("Usuario", value="avnadmin")
db_password = st.sidebar.text_input("Contraseña", type="password") #La contraseña va cambiando, por ello se deja el campo vacío.
db_name = st.sidebar.text_input("Base de Datos", value="defaultdb")

btn_conectar = st.sidebar.button("¡Verificar y Conectar!")

# Gestión del estado para evitar reconexiones.
if "conexion_ok" not in st.session_state:
    st.session_state.conexion_ok = False
    st.session_state.credenciales = {}

# Lógica de conexión tras validar credenciales.
if btn_conectar:
    with st.sidebar.spinner("Conectando a Aiven mediante PyMySQL..."):
        conexion = conectar_base_datos(db_host, db_port, db_user, db_password, db_name)
        if conexion:
            st.session_state.conexion_ok = True
            st.session_state.credenciales = {
                "host": db_host, "port": db_port, "user": db_user, 
                "password": db_password, "database": db_name
            }
            st.sidebar.success("✅ Conexión establecida con éxito.")
            conexion.close() 

# Render de la interfaza gráfica si la conexión es exitosa. Si no lo es, se deja al usuario en espera.
if st.session_state.conexion_ok:
    creds = st.session_state.credenciales
    conexion = conectar_base_datos(creds["host"], creds["port"], creds["user"], creds["password"], creds["database"])

    if conexion:
        st.subheader("📊 Explorador de Base de Datos")
        listado_tablas = obtener_tablas(conexion)
        
        if listado_tablas:
            col_sel, col_btn = st.columns([3, 1])
            with col_sel:
                tabla_seleccionada = st.selectbox("Selecciona una tabla para verificar sus datos:", listado_tablas)
                btn_actualizar = st.button("Actualizar Datos")
            
            with col_btn:
                st.write("##")
            
            if tabla_seleccionada:
                if btn_actualizar:
                    st.toast("Solicitando datos desde Aiven...")
                
                with st.spinner(f"Consultando registros de '{tabla_seleccionada}'..."):
                    df_datos = consultar_tabla(conexion, tabla_seleccionada)
                                                        
                if df_datos is not None:
                    col1, col2 = st.columns(2)
                    col1.metric(label="Registros Auditados", value=len(df_datos))
                    col2.metric(label="Campos / Columnas", value=len(df_datos.columns))
                    
                    # Despliegue del DataFrame.
                    st.write("### Vista previa de los datos en la nube:")
                    st.dataframe(df_datos, use_container_width=True)
                    
                    # Sección de visualización gráfica 
                    st.write("### Representación Gráfica de los Datos:")
                    columnas_numericas = df_datos.select_dtypes(include=['number']).columns.tolist()
                    
                    if columnas_numericas:
                        col_grafico = st.selectbox("Elige la columna numérica para renderizar el gráfico:", columnas_numericas)
                        st.bar_chart(df_datos[col_grafico])
                    else:
                        st.info("Esta tabla no contiene campos numéricos.")
        else:
            st.warning("⚠️ La base de datos no contiene tablas en este momento.")
        conexion.close()
else:
    # Mensaje de espera.
    st.info("--Estado actual: Desconectado. Rellena los datos en el panel izquierdo para vincular con Aiven MySQL.--")