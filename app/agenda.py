from cita import Cita
from cita_urgente import CitaUrgente

from rich.console import Console
from datetime import timedelta

console = Console()

class Agenda:
    def __init__(self):
        # Diccionario donde la clave es el ID del médico y el valor es una lista de citas para ese médico
        self.citas = {}


    def agendar_cita(self, cita):
        if not isinstance(cita, Cita):
            raise TypeError("El objeto proporcionado no es una instancia de la clase Cita")

        medico_id = cita.medico.identificacion
        if medico_id not in self.citas:
            self.citas[medico_id] = []

        self.citas[medico_id].append(cita)

        console.print(f"[green]Cita agendada: {cita}[/green]")

    def encontrar_siguiente_horario_disponible(self, medico, fecha_hora):
        medico_id = medico.identificacion
        nueva_fecha = fecha_hora

        while True:
            nueva_fecha += timedelta(hours=1)
            if not any(
                c.fecha_hora == nueva_fecha for c in self.citas.get(medico_id, [])
            ):
                return nueva_fecha

    def cancelar_cita(self, cita, motivo):
        medico_id = cita.medico.identificacion
        if cita in self.citas.get(medico_id, []):
            self.citas[medico_id].remove(cita)
            cita.motivo_cancelacion = motivo
            console.print(f"[red]Cita cancelada: {cita}[/red]")
        else:
            console.print("[red]La cita no existe en la agenda.[/red]")

    def mover_cita(self, cita, nueva_fecha_hora):
        medico_id = cita.medico.identificacion
        if cita in self.citas.get(medico_id, []):
            cita.fecha_hora = nueva_fecha_hora
            console.print(f"[blue]Cita movida: {cita}[/blue]")
        else:
            console.print("[red]La cita no existe en la agenda.[/red]")

    def buscar_citas_paciente(self, paciente):
        # Buscar citas en todas las listas de médicos
        return [cita for citas in self.citas.values() for cita in citas if cita.paciente == paciente]

    def buscar_citas_medico(self, medico):
        # Obtener citas del médico específico
        return self.citas.get(medico.identificacion, [])
        
    # Método para buscar una cita por su ID
    def buscar_cita_por_id(self, cita_id):
        for citas in self.citas.values():
            for cita in citas:
                if cita.id == cita_id:  # Suponiendo que `id` es un atributo único de Cita
                    return cita
        return None  # Retorna None si no se encuentra la cita

