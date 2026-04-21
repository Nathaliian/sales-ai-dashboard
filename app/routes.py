from fastapi import APIRouter
from app.ai import generate_sql, explain_result
from app.utils import run_query

router = APIRouter()


@router.get("/ask")
def ask(question: str):
    try:
        sql = generate_sql(question)

        data = run_query(sql)

        if isinstance(data, str):
            return {"error": data, "sql": sql}

        insight = explain_result(question, data)

        return {
            "question": question,
            "sql": sql,
            "data": data.to_dict(orient="records"),
            "insight": insight
        }

    except Exception as e:
        return {"error": str(e)}