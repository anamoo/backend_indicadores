from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# -----------------------------
# Tabla carreras
# -----------------------------
class Carrera(Base):
    __tablename__ = "carreras"

    id_carrera = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    egresados = relationship("Egresado", back_populates="carrera")
    titulados = relationship("Titulado", back_populates="carrera")
    matriculas = relationship("Matricula", back_populates="carrera")

# -----------------------------
# Tabla periodos
# -----------------------------
class Periodo(Base):
    __tablename__ = "periodos"

    id_periodo = Column(Integer, primary_key=True, index=True)
    anio = Column(Integer, nullable=False)
    semestre = Column(Integer, nullable=False)
    nombre = Column(String, nullable=False)

    egresados = relationship("Egresado", back_populates="periodo")
    titulados = relationship("Titulado", back_populates="periodo")
    matriculas = relationship("Matricula", back_populates="periodo")
    docentes = relationship("Docente", back_populates="periodo")

# -----------------------------
# Tabla egresados
# -----------------------------
class Egresado(Base):
    __tablename__ = "egresados"

    id_egresado = Column(Integer, primary_key=True, index=True)

    id_carrera = Column(
        Integer,
        ForeignKey("carreras.id_carrera"),
        nullable=False
    )

    id_periodo = Column(
        Integer,
        ForeignKey("periodos.id_periodo"),
        nullable=False
    )

    cantidad = Column(Integer, nullable=False)

    # Relaciones ORM
    carrera = relationship("Carrera", back_populates="egresados")
    periodo = relationship("Periodo", back_populates="egresados")

# -----------------------------
# Tabla titulados
# -----------------------------
class Titulado(Base):
    __tablename__ = "titulados"

    id_titulado = Column(Integer, primary_key=True, index=True)

    id_carrera = Column(
        Integer,
        ForeignKey("carreras.id_carrera"),
        nullable=False
    )

    id_periodo = Column(
        Integer,
        ForeignKey("periodos.id_periodo"),
        nullable=False
    )

    cantidad = Column(Integer, nullable=False)

        # Relaciones ORM
    carrera = relationship("Carrera", back_populates="titulados")
    periodo = relationship("Periodo", back_populates="titulados")

# -----------------------------
# Tabla matriculas
# -----------------------------
class Matricula(Base):
    __tablename__ = "matriculas"

    id_matricula = Column(Integer, primary_key=True, index=True)

    id_carrera = Column(
        Integer,
        ForeignKey("carreras.id_carrera"),
        nullable=False
    )

    id_periodo = Column(
        Integer,
        ForeignKey("periodos.id_periodo"),
        nullable=False
    )

    ni_h = Column(Integer, nullable=False)
    ni_m = Column(Integer, nullable=False)
    re_h = Column(Integer, nullable=False)
    re_m = Column(Integer, nullable=False)
    total_ni = Column(Integer, nullable=False)
    total_re = Column(Integer, nullable=False)

    carrera = relationship("Carrera", back_populates="matriculas")
    periodo = relationship("Periodo", back_populates="matriculas")
   
# -----------------------------
# Tabla departamentos
# -----------------------------
class Departamento(Base):
    __tablename__ = "deptos"

    id_depto = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    docentes = relationship("Docente", back_populates="departamento")

# -----------------------------
# Tabla docentes
# -----------------------------
class Docente(Base):
    __tablename__ = "docentes"

    id_docente = Column(Integer, primary_key=True, index=True)

    id_depto = Column(
        Integer,
        ForeignKey("deptos.id_depto"),
        nullable=False
    )

    id_periodo = Column(
        Integer,
        ForeignKey("periodos.id_periodo"),
        nullable=False
    )

    tc = Column(Integer, nullable=False)
    ct = Column(Integer, nullable=False)
    mt = Column(Integer, nullable=False)
    ha = Column(Integer, nullable=False)
    cantidad = Column(Integer, nullable=False)

    departamento = relationship("Departamento", back_populates="docentes")
    periodo = relationship("Periodo")

# -----------------------------
# Tabla edificios
# -----------------------------

class Edificio(Base):
    __tablename__ = "edificios"

    id_edificio = Column(Integer, primary_key=True, index=True)
    nomenclatura = Column(String(10), nullable=False)
    fundacion = Column(Integer, nullable=False)
    area = Column(Integer, nullable=False)
    alberga = Column(String(200))
    niveles = Column(Integer)

# -----------------------------
# Tabla administrativos
# -----------------------------

class Administrativo(Base):
    __tablename__ = "administrativos"

    id_admtvo = Column(Integer, primary_key=True, index=True)
    h_adm = Column(Integer, nullable=False)
    m_adm = Column(Integer, nullable=False)
    cantidad = Column(Integer, nullable=False)
    
    id_periodo = Column(
        Integer,
        ForeignKey("periodos.id_periodo"),
        nullable=False
    )

    periodo = relationship("Periodo")