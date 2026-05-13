from fastapi import APIRouter, Depends
from fastapi import HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models import Matricula, Egresado, Titulado, Carrera, Periodo, Departamento, Docente, Edificio, Administrativo
from app.schemas import EgresadosResponse, TituladosResponse, MatriculaSexoResponse, DocentesResponse, AdministrativosResponse, EdificiosResponse

router = APIRouter(
    prefix="/indicadores",
    tags=["Indicadores"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/egresados")
def consultar_egresados(
    carrera: str = Query(..., min_length=3, description="Nombre o parte del nombre de la carrera"),
    anio: int = Query(..., ge=1983, le=2100),
    semestre: int = Query(..., ge=1, le=2),
    db: Session = Depends(get_db)
):
    # 1. Buscar carrera (búsqueda flexible)
    carrera_db = (
        db.query(Carrera)
        .filter(Carrera.nombre.ilike(f"%{carrera}%"))
        .first()
    )

    if not carrera_db:
        raise HTTPException(
            status_code=404,
            detail="Carrera no encontrada"
        )

    # 2. Buscar periodo
    periodo_db = (
        db.query(Periodo)
        .filter(
            Periodo.anio == anio,
            Periodo.semestre == semestre,
        )
        .first()
    )

    if not periodo_db:
        raise HTTPException(
            status_code=404,
            detail="Periodo no encontrado"
        )

    # 3. Buscar egresados
    egresados = (
        db.query(Egresado)
        .filter(
            Egresado.id_carrera == carrera_db.id_carrera,
            Egresado.id_periodo == periodo_db.id_periodo
        )
        .first()
    )

    # 4. TOTAL INSTITUCIONAL
    total_egresados = (
        db.query(func.sum(Egresado.cantidad))
        .filter(Egresado.id_periodo == periodo_db.id_periodo)
        .scalar()
    )

    if not egresados:
        raise HTTPException(
            status_code=404,
            detail="No existen datos de egresados para los criterios solicitados"
        )

    # 5. Respuesta
    return {
        "carrera": carrera_db.nombre,
        "anio": periodo_db.anio,
        "periodo": periodo_db.semestre,
        "cantidad_egresados": egresados.cantidad,
        "semestre":periodo_db.nombre,
        "total_institucional": total_egresados or 0
    }

@router.get("/titulados")
def consultar_titulados(
    carrera: str = Query(..., min_length=3),
    anio: int = Query(..., ge=1983, le=2100),
    semestre: int = Query(..., ge=1, le=2),
    db: Session = Depends(get_db)
):
    # 1. Buscar carrera (búsqueda flexible)
    carrera_db = (
        db.query(Carrera)
        .filter(Carrera.nombre.ilike(f"%{carrera}%"))
        .first()
    )

    if not carrera_db:
        raise HTTPException(
            status_code=404,
            detail="Carrera no encontrada"
        )

    # 2. Buscar periodo
    periodo_db = (
        db.query(Periodo)
        .filter(
            Periodo.anio == anio,
            Periodo.semestre == semestre
        )
        .first()
    )

    if not periodo_db:
        raise HTTPException(
            status_code=404,
            detail="Periodo no encontrado"
        )

    # 3. Buscar titulados
    titulados = (
        db.query(Titulado)
        .filter(
            Titulado.id_carrera == carrera_db.id_carrera,
            Titulado.id_periodo == periodo_db.id_periodo
        )
        .first()
    )

    # 4. TOTAL INSTITUCIONAL
    total_titulados = (
        db.query(func.sum(Titulado.cantidad))
        .filter(Titulado.id_periodo == periodo_db.id_periodo)
        .scalar()
    )

    if not titulados:
        raise HTTPException(
            status_code=404,
            detail="No existen datos de titulados para los criterios solicitados"
        )

    # 5. Respuesta
    return {
        "carrera": carrera_db.nombre,
        "anio": periodo_db.anio,
        "periodo": periodo_db.semestre,
        "cantidad_titulados": titulados.cantidad,
        "semestre":periodo_db.nombre,
        "total_institucional": total_titulados or 0
    }

@router.get("/matricula/sexo")
def consultar_matricula_sexo(
    carrera: str = Query(None),
    anio: int = Query(..., ge=1983, le=2100),
    semestre: int = Query(..., ge=1, le=2),
    db: Session = Depends(get_db)
):
    # 1. Buscar periodo
    periodo_db = (
        db.query(Periodo)
        .filter(
            Periodo.anio == anio,
            Periodo.semestre == semestre
        )
        .first()
    )

    if not periodo_db:
        raise HTTPException(404, "Periodo no encontrado")

    # 🔵 CASO 1: MATRÍCULA TOTAL (SIN CARRERA)
    if not carrera:

        resultados = (
            db.query(
                func.sum(Matricula.ni_h).label("ni_h"),
                func.sum(Matricula.ni_m).label("ni_m"),
                func.sum(Matricula.re_h).label("re_h"),
                func.sum(Matricula.re_m).label("re_m"),
                func.sum(Matricula.total_ni).label("total_ni"),
                func.sum(Matricula.total_re).label("total_re")
            )
            .filter(Matricula.id_periodo == periodo_db.id_periodo)
            .first()
        )

        return {
            "tipo": "total",
            "anio": periodo_db.anio,
            "semestre": periodo_db.nombre,
            "hombres": (resultados.ni_h or 0) + (resultados.re_h or 0),
            "mujeres": (resultados.ni_m or 0) + (resultados.re_m or 0),
            "total": (resultados.total_ni or 0) + (resultados.total_re or 0)
        }

    # 🟢 CASO 2: MATRÍCULA POR CARRERA

    carrera_db = (
        db.query(Carrera)
        .filter(Carrera.nombre.ilike(f"%{carrera}%"))
        .first()
    )

    if not carrera_db:
        raise HTTPException(404, "Carrera no encontrada")

    matricula = (
        db.query(Matricula)
        .filter(
            Matricula.id_carrera == carrera_db.id_carrera,
            Matricula.id_periodo == periodo_db.id_periodo
        )
        .first()
    )

    if not matricula:
        raise HTTPException(404, "No hay datos")

    return {
        "tipo": "carrera",
        "carrera": carrera_db.nombre,
        "anio": periodo_db.anio,
        "semestre": periodo_db.nombre,
        "nuevo_ingreso": {
            "hombres": matricula.ni_h,
            "mujeres": matricula.ni_m
        },
        "reingreso": {
            "hombres": matricula.re_h,
            "mujeres": matricula.re_m
        },
        "totales": {
            "total_nuevo_ingreso": matricula.total_ni,
            "total_reingreso": matricula.total_re,
            "Matricula TOTAL": matricula.total_ni + matricula.total_re
        }
    }

@router.get("/matricula/comparativa")
def comparar_matricula(
    carrera: str = Query(..., min_length=3),
    anios: list[int] = Query(...),
    db: Session = Depends(get_db)
):

    # 1. Buscar carrera
    carrera_db = (
        db.query(Carrera)
        .filter(Carrera.nombre.ilike(f"%{carrera}%"))
        .first()
    )

    if not carrera_db:
        raise HTTPException(404, "Carrera no encontrada")

    resultados = []

    for anio in anios:

        periodos = (
            db.query(Periodo)
            .filter(Periodo.anio == anio)
            .all()
        )

        total_anio = 0

        for periodo in periodos:

            matricula = (
                db.query(Matricula)
                .filter(
                    Matricula.id_carrera == carrera_db.id_carrera,
                    Matricula.id_periodo == periodo.id_periodo
                )
                .first()
            )

            if matricula:
                total_anio += (matricula.total_ni or 0) + (matricula.total_re or 0)

        resultados.append({
            "anio": anio,
            "total_matricula": total_anio
        })

    anios_list = [r["anio"] for r in resultados]
    valores_list = [r["total_matricula"] for r in resultados]

    return {
        "carrera": carrera_db.nombre,
        "anios": anios_list,
        "valores": valores_list
    }

@router.get("/docentes")
def consultar_docentes(
    departamento: str = Query(..., min_length=3),
    anio: int = Query(..., ge=2000, le=2100),
    semestre: int = Query(..., ge=1, le=2),
    db: Session = Depends(get_db)
):
    # 1. Buscar departamento (búsqueda flexible)
    depto_db = (
        db.query(Departamento)
        .filter(Departamento.nombre.ilike(f"%{departamento}%"))
        .first()
    )

    if not depto_db:
        raise HTTPException(404, "Departamento no encontrado")

    # 2. Buscar periodo
    periodo_db = (
        db.query(Periodo)
        .filter(
            Periodo.anio == anio,
            Periodo.semestre == semestre
        )
        .first()
    )

    if not periodo_db:
        raise HTTPException(404, "Periodo no encontrado")

    # 3. Buscar docentes
    docentes_db = (
        db.query(
            func.sum(Docente.tc).label("tc"),
            func.sum(Docente.ct).label("ct"),
            func.sum(Docente.mt).label("mt"),
            func.sum(Docente.ha).label("ha"),
            func.sum(Docente.cantidad).label("total")
        )
        .filter(
            Docente.id_depto == depto_db.id_depto,
            Docente.id_periodo == periodo_db.id_periodo
        )
        .first()
    )

    if not docentes_db or not docentes_db.total:
        raise HTTPException(
            404,
            "No existen datos de docentes para los criterios solicitados"
        )

    # 4. Respuesta
    return {
        "departamento": depto_db.nombre,
        "anio": periodo_db.anio,
        "semestre": periodo_db.nombre,
        "tiempo_completo": docentes_db.tc or 0,
        "tres_cuartos_tiempo": docentes_db.ct or 0,
        "medio_tiempo": docentes_db.mt or 0,
        "horas_asignatura": docentes_db.ha or 0,
        "total_docentes": docentes_db.total or 0
    }

@router.get("/administrativos")
def consultar_administrativos(
    anio: int = Query(..., ge=2000, le=2100),
    semestre: int = Query(..., ge=1, le=2),
    db: Session = Depends(get_db)
):
    # 2. Buscar periodo
    periodo_db = (
        db.query(Periodo)
        .filter(
            Periodo.anio == anio,
            Periodo.semestre == semestre
        )
        .first()
    )

    if not periodo_db:
        raise HTTPException(404, "Periodo no encontrado")

    # 3. Buscar administrativos
    administrativos_db = (
        db.query(
            func.sum(Administrativo.h_adm).label("h_adm"),
            func.sum(Administrativo.m_adm).label("m_adm"),
            func.sum(Administrativo.cantidad).label("total"),
        
        )
        .filter(
            Administrativo.id_periodo == periodo_db.id_periodo
        )
        .first()
    )

    if not administrativos_db or not administrativos_db.total:
        raise HTTPException(
            404,
            "No existen datos de administrativos para los criterios solicitados"
        )

    # 4. Respuesta
    return {
        "anio": periodo_db.anio,
        "semestre": periodo_db.nombre,
        "hombres_adm": administrativos_db.h_adm or 0,
        "mujeres_adm": administrativos_db.m_adm or 0,
        "total_adm": administrativos_db.total or 0
    }

@router.get("/edificios")
def consultar_edificio(
    nomenclatura: str | None = Query(None),
    fundacion: int | None = Query(None),
    alberga: str | None = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(Edificio)

    # filtro por nomenclatura
    if nomenclatura:
        query = query.filter(
            Edificio.nomenclatura.ilike(f"{nomenclatura}")
        )

    # filtro por año de fundación
    if fundacion:
        query = query.filter(
            Edificio.fundacion == fundacion
        )

    # filtro por lo que alberga
    if alberga:

        if alberga == "lab":
            query = query.filter(Edificio.alberga.ilike("%lab%"))

        elif alberga == "aulas":
            query = query.filter(Edificio.alberga.ilike("%aula%"))

        elif alberga == "oficinas":
            query = query.filter(Edificio.alberga.ilike("%oficina%"))
       
        elif alberga == "taller":
            query = query.filter(Edificio.alberga.ilike("%taller%"))

    edificios = query.all()

    if not edificios:
        return []

    resultados = []

    for edificio in edificios:
        resultados.append({
            "id_edificio": edificio.id_edificio,
            "nomenclatura": edificio.nomenclatura,
            "fundacion": edificio.fundacion,
            "area": edificio.area,
            "alberga": edificio.alberga,
            "niveles": edificio.niveles
        })

    return resultados