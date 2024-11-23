from datetime import datetime
from rich import print
from rich.console import Console
from hospital import Hospital
from paciente import Paciente
from medico import Medico
from cita import Cita
from flask import Flask, render_template, request, redirect, url_for, flash


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash messages


console = Console()


def cargar_datos_iniciales():
    hospital = Hospital()

    # Cargar pacientes iniciales
    hospital.cargar_pacientes_desde_csv("data/pacientes.csv")

    # Cargar médicos iniciales
    hospital.cargar_medicos_desde_json("data/medicos.json")

    # Cargar citas iniciales
    hospital.cargar_citas_desde_csv("data/citas.csv")

    return hospital



def mostrar_lista_pacientes(hospital):
    lista_pacientes = []
    for paciente in hospital.pacientes:
        lista_pacientes.append({
            "id": paciente.identificacion,
            "nombre": paciente.nombre,
            "celular": paciente.celular,
            "correo": paciente.correo
        })
    return lista_pacientes

    


def mostrar_lista_medicos(hospital):
    lista_medicos = []
    for medico in hospital.medicos:
        lista_medicos.append({
            "id": medico.identificacion,
            "nombre": medico.nombre,
            "celular": medico.celular,
            "especialidad": medico.especialidad
        })
    return lista_medicos


def mostrar_lista_citas(hospital):
    lista_citas = []
    for cita in hospital.agenda.citas:
        lista_citas.append({
            "id": cita.paciente.identificacion,
            "nombre": cita.paciente.nombre,
            "medico": cita.medico.nombre,
            "especialidad": cita.medico.especialidad,
            "fecha_hora": cita.fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
            "urgente": "SÍ" if str(type(cita).__name__) == "CitaUrgente" else "NO"
        })
    return lista_citas




# Esto es lo que he modificado
hospital = cargar_datos_iniciales()

@app.route('/')
def mostrar_menu():
    return render_template('index.html')
        
            
        

#pacientes   
#agregar paciente
@app.route('/agregar_paciente', methods=['GET', 'POST'])
def agregar_paciente():
    if request.method == 'POST':
        identificacion = request.form['identificacion']
        nombre = request.form['nombre']
        celular = request.form['celular']
        correo = request.form['correo']
        paciente = Paciente(identificacion, nombre, celular, correo)
        hospital.agregar_paciente(paciente)
        flash('Paciente agregado exitosamente')   
    return render_template('agregar_paciente.html')  # Formulario para agregar paciente

#cita del paciente 
@app.route('/cita_paciente', methods=['GET', 'POST'])
def cita_paciente():
    if request.method == 'POST':
        idPaciente = request.form.get('identificacion')
        paciente = hospital.buscar_paciente(idPaciente)
        
        if paciente:
            # Busca todas las citas del paciente
            citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
            
            if citas_paciente:
                # Pasa el paciente y todas sus citas a la plantilla
                return render_template('cita_paciente.html', paciente=paciente, citas=citas_paciente)
            else:
                flash("El paciente no tiene citas programadas")
                return redirect(url_for('cita_paciente'))
        else:
            flash("No se encontró el paciente con la identificación ingresada")
            return redirect(url_for('cita_paciente'))
    
    return render_template('cita_paciente.html')  # Formulario de búsqueda


#buscar paciente
@app.route('/buscar_paciente', methods=['GET','POST'])
def buscar_paciente():
    if request.method == 'POST':
        identificacion = request.form.get('identificacion')
        paciente = hospital.buscar_paciente(identificacion)
        
        if paciente:
            # Pasar un solo paciente como contexto
            return render_template('buscar_paciente.html', paciente=paciente)
        else:
            flash('No se encontró el paciente con la identificación ingresada')
            return redirect(url_for('buscar_paciente'))
    
    # Renderizar el formulario en el método GET sin ningún paciente
    return render_template('buscar_paciente.html')
@app.route('/lista_paciente')
def lista_paciente():
    pacientes = mostrar_lista_pacientes(hospital)
    return render_template('lista_paciente.html', pacientes=pacientes)  # Lista de pacientes

#///////////////////////////////////////////////////////////////

#medicos
#agregar medicos
@app.route('/agregar_medico', methods=['GET', 'POST'])
def agregar_medico():
    if request.method == 'POST':
        identificacion = request.form['identificacion']
        nombre = request.form['nombre']
        celular = request.form['celular']
        especialidad = request.form['especialidad']
        medico = Medico(identificacion, nombre, celular, especialidad)
        hospital.agregar_medico(medico)
        flash('Médico agregado exitosamente')
    return render_template('agregar_medico.html')  # Formulario para agregar médico
#lista de los medicos
@app.route('/lista_medico', methods=['GET', 'POST'])
def lista_medico():
    medicos = mostrar_lista_medicos(hospital)
    return render_template('lista_medico.html', medicos=medicos)  # Lista de médicos
#buscar medicos
@app.route('/buscar_medico', methods=['GET', 'POST'])
def buscar_medico():
    if request.method == 'POST':

        identificacion = request.form.get('identificacion')
        medico = hospital.buscar_medico(identificacion)
        print(medico)
        if medico:
            # Pasar un solo médico como contexto
            return render_template('buscar_medico.html', medico=medico)
        else:
            flash('No se encontró el médico con la identificación ingresada')
            return redirect(url_for('buscar_medico'))
   
    
    # Renderizar el formulario en el método GET sin ningún médico
    return render_template('buscar_medico.html')
#citas del medico
@app.route('/citas_medico', methods=['GET', 'POST'])
def citas_medico():
    if request.method == 'POST':
        idMedico = request.form.get('identificacion')
        medico = hospital.buscar_medico(idMedico)
        
        if medico:
            # Busca todas las citas del médico
            
            citas_medico = hospital.agenda.buscar_citas_medico(medico)
            
            if citas_medico:
                # Pasa el médico y todas sus citas a la plantilla
                return render_template('citas_medico.html', medico=medico, citas=citas_medico)
            else:
                flash("El médico no tiene citas programadas")
                return redirect(url_for('citas_medico'))
        else:
            flash("No se encontró el médico con la identificación ingresada")
            return redirect(url_for('citas_medico'))
    
    return render_template('citas_medico.html')  # Formulario de búsqueda

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#citas
@app.route('/agendar_cita', methods=['GET', 'POST'])
def agendar_cita():
    if request.method == 'POST':
               # Recibir datos del formulario
        """         idpaciente = request.form.get('identificacion')
        especialidad = request.form.get('especialidad')
        medico_id = request.form.get('medico')
        fecha_hora = request.form.get('fecha_hora')

        # Imprimir los datos recibidos en la consola
        print("Datos recibidos:")
        print(f"ID del paciente: {idpaciente}")
        print(f"Especialidad: {especialidad}")
        print(f"ID del médico: {medico_id}")
        print(f"Fecha y hora (str): {fecha_hora}") 
        """
        # Recibir datos del formulario
        idpaciente = request.form.get('identificacion')
        paciente = hospital.buscar_paciente(idpaciente)

        if paciente:
            especialidad = request.form.get('especialidad')
            medico_id = request.form.get('medico')
            fecha_hora = request.form.get('fecha_hora')
            urgente= request.form.get('urgente')

        # Validar si la cita es urgente, asegurándonos de que sea una cadena antes de .lower()
            urgente = urgente.lower() == 'sí' 

            
            # Buscar médico por id
            medico = hospital.buscar_medico(medico_id)

            if medico:
                try:
                    # Convertir fecha_hora a datetime
                    fecha_hora = datetime.strptime(fecha_hora, "%Y-%m-%dT%H:%M:%S")

                    # Validar si la fecha y hora es futura
                    if fecha_hora < datetime.now():
                        flash("fecha elegida no es correcta, intentalo de nuevo ",'error')
                        return redirect(url_for('agendar_cita'))
                    
                    # Validar que los minutos sean 0,20,40 (intervalos de 20 minutos)
                    if fecha_hora.minute not in [0, 20, 40]:
                        flash('La cita debe ser agendada en intervalos de 20 minutos (00, 20, 40).', 'error')
                        return redirect(url_for('agendar_cita'))

                    # Crear la cita
                    cita = Cita(paciente=paciente, medico=medico, fecha_hora=fecha_hora, urgente=urgente)
                    hospital.agenda.agendar_cita(cita)

                    # Crear un mensaje de éxito detallado
                    tipo_cita = "urgente" if urgente else "regular"
                    mensaje_exito = (
                        f"Cita {tipo_cita} agendada exitosamente para el paciente {paciente.nombre} "
                        f"con el Dr. {medico.nombre} en la especialidad de {especialidad} "
                        f"programada para el {fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}"
                    )

                    flash(mensaje_exito, 'success')
                except ValueError:
                    flash('Formato de fecha y hora inválido. Use AAAA-MM-DD HH:MM:SS', 'error')
            else:
                flash('Médico no encontrado', 'error')
        else:
            flash('Paciente no encontrado', 'error')

    # Obtener las especialidades disponibles
    especialidades = hospital.obtener_especialidades_disponibles()

    # Obtener médicos por especialidad
    medicos_por_especialidad = {
        especialidad: [medico.to_dict() for medico in hospital.buscar_medicos_por_especialidad(especialidad)]
        for especialidad in especialidades
    }

    return render_template('agendar_cita.html', especialidades=especialidades, medicos_por_especialidad=medicos_por_especialidad)

@app.route('/buscar_citas_paciente', methods=['POST'])
def buscar_citas_paciente():
    idpaciente = request.form.get('identificacion')
    paciente = hospital.buscar_paciente(idpaciente)

    if paciente:
        citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
        if citas_paciente:
            return render_template('feedback.html', paciente=paciente, citas=citas_paciente)
        else:
            flash('No hay citas para este paciente', 'error')
    else:
        flash('Paciente no encontrado', 'error')
    
    return redirect(url_for('feedback'))

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Obtener datos del formulario
        cita_info = request.form.get('cita_id')  # Formato: medico_nombre|paciente_nombre|fecha_hora
        calificacion = request.form.get('calificacion')
        comentario = request.form.get('comentario')

        # Validar campos
        if not cita_info or not calificacion or not comentario:
            flash('Por favor complete todos los campos del formulario.', 'error')
            return redirect(url_for('feedback'))

        try:
            # Dividir y procesar cita_info
            medico_nombre, paciente_nombre, fecha_hora = cita_info.split('|')
            fecha_hora = datetime.strptime(fecha_hora.strip(), '%Y-%m-%d %H:%M:%S')

            # Buscar al paciente por nombre
            paciente = next((p for p in hospital.pacientes if p.nombre == paciente_nombre), None)
            if not paciente:
                flash('Paciente no encontrado.', 'error')
                return redirect(url_for('feedback'))

            # Buscar las citas del paciente
            citas_paciente = hospital.agenda.buscar_citas_paciente(paciente)
            if not citas_paciente:
                flash('El paciente no tiene citas disponibles para calificar.', 'error')
                return redirect(url_for('feedback'))

            # Buscar la cita seleccionada
            cita_seleccionada = next(
                (c for c in citas_paciente
                 if c.medico.nombre == medico_nombre and c.fecha_hora == fecha_hora),
                None
            )

            if not cita_seleccionada:
                flash('Cita no encontrada.', 'error')
                return redirect(url_for('feedback'))

            # Verificar si ya tiene feedback
            if cita_seleccionada.feedback:
                flash('Esta cita ya tiene una calificación asignada.', 'error')
                return redirect(url_for('feedback'))
            print(f"cita: { cita_seleccionada}")
            print(f"cita: { calificacion}")
            print(f"comentario: {comentario}")
            # Agregar feedback
            hospital.agregar_feedback_cita(cita_seleccionada, int(calificacion), comentario.strip())
            flash('Feedback agregado con éxito.', 'success')

        except ValueError as e:
            flash(f"Error procesando los datos: {e}", 'error')

        return redirect(url_for('feedback'))

    # Método GET: Mostrar formulario
    paciente = None
    citas = []
    if 'paciente_id' in request.args:
        paciente_id = request.args.get('paciente_id')
        paciente = hospital.buscar_paciente(paciente_id.strip())
        if paciente:
            citas = hospital.agenda.buscar_citas_paciente(paciente)

    return render_template('feedback.html', paciente=paciente, citas=citas)



# ver calificacion de la cita
@app.route('/ver_calificacion', methods=['GET', 'POST'])
def ver_calificacion():
    lista_medicos = []

    for medico in hospital.medicos:
        calificacion_promedio = round(medico.calificacion_promedio())
        lista_medicos.append({
            'nombre': medico.nombre,
            'especialidad': medico.especialidad,
            'calificacion': calificacion_promedio
        })

    return render_template('ver_calificacion.html', medicos=lista_medicos)


    

if __name__ == "__main__":
    app.run(debug=True)
