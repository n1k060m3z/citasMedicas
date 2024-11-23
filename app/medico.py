from persona import Persona


class Medico(Persona):
    def __init__(self, identificacion, nombre, celular, especialidad):
        super().__init__(identificacion, nombre, celular)
        self.especialidad = especialidad
        self.calificaciones = []
        
    
    def to_dict(self):
        """Convierte el objeto Medico en un diccionario serializable."""
        return {
            'id': self.identificacion,
            'nombre': self.nombre,
            'celular': self.celular,
            'especialidad': self.especialidad,
        }

    def calificacion_promedio(self):
        if not self.calificaciones:
            return 0
        return sum(self.calificaciones) / len(self.calificaciones)
