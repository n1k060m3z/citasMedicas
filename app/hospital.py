import csv
import json
from agenda import Agenda
from paciente import Paciente
from cita import Cita
from cita_urgente import CitaUrgente
from medico import Medico
from datetime import datetime
from rich import print
from rich.console import Console

console = Console()


class Hospital:
    def __init__(self):
        self.pacientes = []
        self.medicos = []
        self.agenda = Agenda()

    def agregar_paciente(self, paciente):
        self.pacientes.append(paciente)
        print(f"[green]Paciente {paciente.nombre} agregado al hospital.[/green]")

    def agregar_medico(self, medico):
        self.medicos.append(medico)

    def buscar_paciente(self, identificacion):
        return next(
            (p for p in self.pacientes if p.identificacion == identificacion), None
        )

    def buscar_medico(self, identificacion):
        return next(
            (m for m in self.medicos if m.identificacion == identificacion), None
        )

    def buscar_medicos_por_especialidad(self, especialidad):
        return [m for m in self.medicos if m.especialidad == especialidad]
    def obtener_especialidades_disponibles(self):
        """Devuelve una lista de especialidades disponibles en el hospital."""
        especialidades = set(m.especialidad for m in self.medicos)
        return list(especialidades)

    def cargar_pacientes_desde_csv(self, archivo):
        try:
            with open(archivo, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    paciente = Paciente(
                        row["identificación"],
                        row["nombre_completo"],
                        row["celular"],
                        row["correo"],
                    )
                    self.agregar_paciente(paciente)
            console.print(
                "[bold][green]Pacientes cargados exitosamente desde el archivo CSV.[/green][/bold]"
            )
        except FileNotFoundError:
            console.print("[red]Error: No se encontró el archivo CSV.[/red]")
        except Exception as e:
            console.print(f"[red]Error al cargar pacientes: {str(e)}[/red]")

    def cargar_medicos_desde_json(self, archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as jsonfile:
                medicos_data = json.load(jsonfile)
                for medico_data in medicos_data:
                    # Asegurarse de que todos los campos necesarios estén presentes
                    if all(
                        key in medico_data
                        for key in ["id", "nombre", "celular", "especialidad"]
                    ):
                        medico = Medico(
                            medico_data["id"],
                            medico_data["nombre"],
                            medico_data["celular"],
                            medico_data["especialidad"],
                        )
                        self.agregar_medico(medico)
                    else:
                        console.print(
                            f"[yellow]Advertencia: Datos incompletos para el médico {medico_data.get('nombre', 'desconocido')}[/yellow]"
                        )
            console.print(
                "[bold][green]Médicos cargados exitosamente desde el archivo JSON.[/green][/bold]"
            )
        except FileNotFoundError:
            console.print("[red]Error: No se encontró el archivo JSON.[/red]")
        except json.JSONDecodeError:
            console.print("[red]Error: El archivo JSON está mal formateado.[/red]")
        except Exception as e:
            console.print(f"[red]Error al cargar médicos: {str(e)}[/red]")

    def cargar_citas_desde_csv(self, archivo_csv):
        citas = []
        with open(archivo_csv, 'r') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                try:
                    # Obtener el ID del médico desde el archivo CSV
                    medico_id = fila['medicos']

                    # Buscar el objeto Medico correspondiente usando el ID (esto depende de cómo cargues tus médicos)
                    medico = self.buscar_medico(medico_id)
                    if not medico:
                        raise ValueError(f"No se encontró el médico con ID {medico_id}")
                    paciente_id = fila['paciente']
                    paciente =self.buscar_paciente(paciente_id)  
                    if paciente and medico:
                         fecha_hora = datetime.strptime(
                            fila["fecha_hora"], "%Y-%m-%d %H:%M:%S"
                         )
                         cita = Cita(paciente, medico, fecha_hora)
                         self.agenda.agendar_cita(cita)
                    urgente = fila.get('urgente', 'False').lower() == 'true'
                    cita = Cita(paciente, medico, fecha_hora, urgente)

                    citas.append(cita)
                except KeyError as e:
                    print(f"Falta un campo requerido en el archivo: {e}")
                except ValueError as e:
                    print(f"Error de formato en la fecha/hora: {e}")
        return citas
    def agregar_feedback_cita(self, cita_seleccionada, calificacion, comentario):
        if cita_seleccionada in self.agenda.citas:
            print(f"Agregando feedback a la cita: {cita_seleccionada}")
            cita_seleccionada.agregar_feedback(calificacion, comentario)
            
            console.print(
                f"[green]Feedback agregado a la cita de {cita_seleccionada.paciente.nombre}[/green]"
            )
        else:
            console.print("[red]La cita no existe en la agenda.[/red]")

def buscar_medico_por_id(self, medico_id):
    # Buscar el médico por su ID en la lista de médicos (o archivo JSON, base de datos, etc.)
    # Este es un ejemplo simple, depende de cómo estés almacenando tus médicos
    for medico in self.medicos:
        if medico.identificacion == medico_id:
            return medico
    return None
        # try:
        #     with open(archivo, newline="", encoding="utf-8") as csvfile:
        #         reader = csv.DictReader(csvfile)
        #         for row in reader:
        #             paciente = self.buscar_paciente(row["paciente"])
        #             medico = self.buscar_medico(row["medicos"])
        #             if paciente and medico:
        #                 fecha_hora = datetime.strptime(
        #                     row["fecha_hora"], "%Y-%m-%d %H:%M:%S"
        #                 )
        #                 cita = Cita(paciente, medico, fecha_hora)
        #                 self.agenda.agendar_cita(cita)
        #             else:
        #                 if not paciente:
        #                     console.print(
        #                         f"[yellow]Advertencia: No se encontró el paciente con ID {row['paciente']}[/yellow]"
        #                     )
        #                 if not medico:
        #                     console.print(
        #                         f"[yellow]Advertencia: No se encontró el médico con ID {row['medicos']}[/yellow]"
        #                     )
        #     console.print(
        #         "[bold][green]Citas cargadas exitosamente desde el archivo CSV.[/green][/bold]"
        #     )
        # except FileNotFoundError:
        #     console.print("[red]Error: No se encontró el archivo CSV de citas.[/red]")
        # except Exception as e:
        #     console.print(f"[red]Error al cargar citas: {str(e)}[/red]")

def agendar_cita_urgente(self, paciente, medico, fecha_hora):
        cita_urgente = CitaUrgente(paciente, medico, fecha_hora)
        self.agenda.agendar_cita(cita_urgente)

"""     def agregar_feedback_cita(self, cita, calificacion, comentario):
        if cita in self.agenda.citas:
            cita.agregar_feedback(calificacion, comentario)
            console.print(
                f"[green]Feedback agregado a la cita de {cita.paciente.nombre}[/green]"
            )
        else:
            console.print("[red]La cita no existe en la agenda.[/red]") """
