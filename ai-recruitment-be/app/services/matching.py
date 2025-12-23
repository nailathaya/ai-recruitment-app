from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("intfloat/multilingual-e5-small")


def build_candidate_text(candidate: dict) -> str:
    skills = ", ".join([s["name"] for s in candidate.get("skills", [])])
    experiences = " ".join([
        f'{e["jobTitle"]} {e.get("description","")}'
        for e in candidate.get("workExperience", [])
    ])
    education = " ".join([
        f'{e["degree"]} {e.get("fieldOfStudy","")}'
        for e in candidate.get("education", [])
    ])

    return f"""
    Skills: {skills}
    Experience: {experiences}
    Education: {education}
    """


def match_candidates(job_description: str, candidates: list):
    job_emb = model.encode(job_description, normalize_embeddings=True)

    results = []
    for c in candidates:
        text = build_candidate_text(c)
        cand_emb = model.encode(text, normalize_embeddings=True)

        score = cosine_similarity([job_emb], [cand_emb])[0][0]

        results.append({
            "id": c["id"],
            "name": c["user"]["name"],
            "score": round(score * 100, 2),
            "raw": c
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)
