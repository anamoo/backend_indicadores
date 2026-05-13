from pydantic import BaseModel

class MatriculaSexoResponse(BaseModel):
    carrera: str
    anio: int
    semestre: int
    nuevo_ingreso: dict
    reingreso: dict
    totales: dict

class EgresadosResponse(BaseModel):
    carrera: str
    anio: int
    semestre: int
    cantidad_egresados: int

class TituladosResponse(BaseModel):
    carrera: str
    anio: int
    semestre: int
    cantidad_titulados: int

class EdificiosResponse(BaseModel):
    nomenclatura: str
    fundacion: int
    area: float
    alberga: str
    niveles: int

class AdministrativosResponse(BaseModel):
    h_adm: int
    m_adm: int
    cantidad: int
    
class DocentesResponse(BaseModel):
    departamento: str
    anio: int
    semestre: int
    tiempo_completo: int
    tres_cuartos_tiempo: int
    medio_tiempo: int
    horas_asignatura: int
    total_docentes: int

    class Config:
        orm_mode = True