"""
seed.py — Popula o banco com dados de teste realistas.
Execute com:  python seed.py
(pode rodar de novo sem duplicar nada — é seguro)
"""

from datetime import date, timedelta

from app import create_app, db
from app.models import (
    Estudante, Responsavel, ProfissionalEducacao,
    Falta, Nota, Observacao, Post, Comentario, Curtida, DISCIPLINAS,
)

app = create_app()

with app.app_context():
    db.create_all()

    # ── Profissionais ────────────────────────────────────────────────────
    if not ProfissionalEducacao.query.filter_by(rg="87654321").first():
        suila = ProfissionalEducacao(
            nome="Suíla Ferreira", rg="87654321",
            cargo="Professora", disciplina="Matemática", sala="Sala 12",
        )
        suila.set_senha("senha123")
        db.session.add(suila)

    if not ProfissionalEducacao.query.filter_by(rg="11223344").first():
        diretor = ProfissionalEducacao(
            nome="Roberto Nascimento", rg="11223344",
            cargo="Diretor", disciplina=None, sala="Secretaria",
        )
        diretor.set_senha("senha123")
        db.session.add(diretor)

    db.session.commit()

    # ── Estudantes (turma 7A) ───────────────────────────────────────────
    dados_estudantes = [
        ("2024001", "Davi Oliveira", "7A", True),    # grêmio
        ("2024002", "Enzo Ramos", "7A", True),        # grêmio
        ("2024003", "Larissa Souza", "7A", False),
        ("2024004", "Pedro Henrique", "7A", False),
        ("2024005", "Marina Costa", "7B", False),
    ]
    for ra, nome, turma, gremio in dados_estudantes:
        if not Estudante.query.filter_by(ra=ra).first():
            est = Estudante(nome=nome, ra=ra, turma=turma, gremio=gremio)
            est.set_senha("senha123")
            db.session.add(est)

    db.session.commit()

    davi = Estudante.query.filter_by(ra="2024001").first()
    enzo = Estudante.query.filter_by(ra="2024002").first()
    larissa = Estudante.query.filter_by(ra="2024003").first()
    suila = ProfissionalEducacao.query.filter_by(rg="87654321").first()

    # ── Responsável (vinculado à Larissa) ───────────────────────────────
    if not Responsavel.query.filter_by(rg="12345678").first():
        resp = Responsavel(nome="Camila Souza", rg="12345678", estudante_id=larissa.id)
        resp.set_senha("senha123")
        db.session.add(resp)

    db.session.commit()

    # ── Faltas de exemplo (Larissa tem 2 faltas registradas) ────────────
    if Falta.query.filter_by(estudante_id=larissa.id).count() == 0:
        db.session.add(Falta(estudante_id=larissa.id, data=date.today() - timedelta(days=5),
                              materia="Matemática", registrada_por=suila.id))
        db.session.add(Falta(estudante_id=larissa.id, data=date.today() - timedelta(days=2),
                              materia="História", registrada_por=suila.id))

    # ── Notas de exemplo ──────────────────────────────────────────────────
    if Nota.query.filter_by(estudante_id=larissa.id).count() == 0:
        exemplos_notas = [
            ("Português", 1, 8.5), ("Matemática", 1, 7.0), ("Ciências", 1, 9.0),
            ("Português", 2, 7.5), ("Matemática", 2, 8.0),
        ]
        for materia, bim, valor in exemplos_notas:
            db.session.add(Nota(estudante_id=larissa.id, materia=materia, bimestre=bim,
                                 valor=valor, atividade="Prova bimestral"))

    # ── Observações de exemplo ───────────────────────────────────────────
    if Observacao.query.filter_by(estudante_id=larissa.id).count() == 0:
        db.session.add(Observacao(estudante_id=larissa.id, profissional_id=suila.id,
                                   texto="Participou bastante da aula de hoje, respondendo às perguntas.",
                                   categoria="participativo"))
        db.session.add(Observacao(estudante_id=larissa.id, profissional_id=suila.id,
                                   texto="Estava mais quieta que o normal, vale conversar com ela.",
                                   categoria="quieto"))

    db.session.commit()

    # ── Posts de exemplo (só grêmio/profissional podem postar) ──────────
    if Post.query.count() == 0:
        p1 = Post(autor_tipo="Estudante", autor_id=davi.id,
                   texto="Pessoal, a Festa Junina está chegando! Fiquem ligados nas novidades do grêmio 🎉")
        p2 = Post(autor_tipo="ProfissionalEducacao", autor_id=suila.id,
                   texto="Lembrando que a prova de Matemática do 2º bimestre será dia 20. Bons estudos!")
        db.session.add_all([p1, p2])
        db.session.commit()

        db.session.add(Comentario(post_id=p1.id, autor_tipo="Estudante", autor_id=enzo.id,
                                   texto="Bora! Já quero saber o tema desse ano"))
        db.session.add(Curtida(post_id=p1.id, autor_tipo="Estudante", autor_id=larissa.id))
        db.session.commit()

    print("✅ Banco populado com sucesso!\n")
    print("   👨‍🎓 Estudante (grêmio) → RA: 2024001  | Senha: senha123  (Davi, pode postar)")
    print("   👨‍🎓 Estudante (grêmio) → RA: 2024002  | Senha: senha123  (Enzo, pode postar)")
    print("   👩‍🎓 Estudante (normal) → RA: 2024003  | Senha: senha123  (Larissa, só comenta/curte)")
    print("   👨‍👩‍👧 Responsável       → RG: 12345678 | Senha: senha123  (mãe da Larissa)")
    print("   👩‍🏫 Profissional       → RG: 87654321 | Senha: senha123  (Suíla, professora)")
    print("   🧑‍💼 Profissional       → RG: 11223344 | Senha: senha123  (Roberto, diretor)")
