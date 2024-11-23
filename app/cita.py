from datetime import datetime
class Cita:
    def __init__(self, paciente, medico, fecha_hora, urgente=False):
        self.paciente = paciente
        self.medico = medico
        # Verifica si fecha_hora es un string y lo convierte a datetime
        if isinstance(fecha_hora, str):
            self.fecha_hora = datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M:%S')
        else:
            self.fecha_hora = fecha_hora
        self.urgente = urgente
        self.motivo_cancelacion = None
        self.calificacion = None
        self.comentario = None
        self.feedback = None  # Feedback inicial vacío

    def __repr__(self):
        tipo_cita = "urgente" if self.urgente else "regular"
        return (f"Cita {tipo_cita} del paciente {self.paciente.nombre} "
                f"con el Dr. {self.medico.nombre} programada para "
                f"{self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}")

    def agregar_feedback(self, calificacion, comentario):
        if self.feedback:
            raise ValueError("Esta cita ya tiene feedback.")  # Evita agregar feedback duplicado
        self.feedback = {"calificacion": calificacion, "comentario": comentario}
