from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import asyncio
import uuid

app = FastAPI(title="Microservicio de Citas Médicas")


class Cita(BaseModel):
    id: str | None = None
    paciente: str
    medico: str
    fecha: str
    motivo: str
    estado: str | None = "Activa"


citas_db: List[Cita] = []



@app.post("/citas", response_model=Cita)
async def crear_cita(cita: Cita):

    
    await asyncio.sleep(2)

    cita.id = str(uuid.uuid4())
    citas_db.append(cita)

    return cita



@app.get("/citas", response_model=List[Cita])
async def listar_citas():

    if not citas_db:
        raise HTTPException(
            status_code=404,
            detail="No hay citas registradas"
        )

    return citas_db



@app.get("/citas/paciente/{nombre}", response_model=List[Cita])
async def buscar_por_paciente(nombre: str):

    resultados = [c for c in citas_db if c.paciente.lower() == nombre.lower()]

    if not resultados:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron citas para este paciente"
        )

    return resultados


@app.delete("/citas/{cita_id}")
async def cancelar_cita(cita_id: str):

    for cita in citas_db:
        if cita.id == cita_id:
            if cita.estado == "Cancelada":
                raise HTTPException(
                    status_code=400,
                    detail="La cita ya está cancelada"
                )

            cita.estado = "Cancelada"
            return {"mensaje": "Cita cancelada correctamente"}

    raise HTTPException(
        status_code=404,
        detail="Cita no encontrada"
    )