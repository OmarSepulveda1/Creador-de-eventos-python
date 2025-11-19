from django.shortcuts import render, redirect
from .forms import EventoForm, ParticipanteForm


def home(request):
    return render(request, 'eventos/home.html')

def registrar_evento(request):
    participante_forms = []

    if request.method == "POST":
        evento_form = EventoForm(request.POST)
        total_participantes = int(request.POST.get("total_participantes", 1))

        # Crear lista de formularios de participantes
        for i in range(total_participantes):
            participante_forms.append(
                ParticipanteForm(request.POST, prefix=f"p{i}")
            )

        if evento_form.is_valid() and all(f.is_valid() for f in participante_forms):
            evento = evento_form.save()

            for form in participante_forms:
                participante = form.save(commit=False)
                participante.evento = evento
                participante.save()

            return redirect("registro_exitoso")

    else:
        evento_form = EventoForm()
        participante_forms = [ParticipanteForm(prefix="p0")]

    return render(request, "evento_form.html", {
        "evento_form": evento_form,
        "participante_forms": participante_forms,
    })


def registro_exitoso(request):
    return render(request, "registro_exitoso.html")
