from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import EventoForm, ParticipanteForm, ParticipanteFormSet
from .models import Evento, Participante


def home(request):
    # Mostrar lista de eventos guardados en la página principal
    eventos = Evento.objects.all().order_by('-fecha')
    return render(request, 'eventos/home.html', {'eventos': eventos})

@login_required(login_url='/admin/login/')
def registrar_evento(request):
    if request.method == "POST":
        evento_form = EventoForm(request.POST)
        participante_formset = ParticipanteFormSet(request.POST, prefix='participants')

        if evento_form.is_valid() and participante_formset.is_valid():
            evento = evento_form.save(commit=False)
            evento.owner = request.user
            evento.save()

            # Crear participantes desde el formset
            for pform in participante_formset:
                nombre = pform.cleaned_data.get('nombre')
                correo = pform.cleaned_data.get('correo')
                if nombre and correo:
                    Participante.objects.create(evento=evento, nombre=nombre, correo=correo)

            return redirect("registro_exitoso")
    else:
        evento_form = EventoForm()
        participante_formset = ParticipanteFormSet(prefix='participants')

    return render(request, "evento_form.html", {
        "evento_form": evento_form,
        "participante_formset": participante_formset,
    })


def registro_exitoso(request):
    return render(request, "registro_exitoso.html")


@login_required(login_url='/admin/login/')
def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    # sólo usuarios admin/staff pueden editar
    if not request.user.is_staff:
        return HttpResponseForbidden('Solo administradores pueden editar este evento')
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventoForm(instance=evento)

    # Reuse the creation template but without participant forms
    return render(request, 'evento_form.html', {
        'evento_form': form,
        'participante_forms': [],
    })


@login_required(login_url='/admin/login/')
def eliminar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    # sólo usuarios admin/staff pueden eliminar
    if not request.user.is_staff:
        return HttpResponseForbidden('Solo administradores pueden eliminar este evento')
    if request.method == 'POST':
        evento.delete()
        return redirect('home')
    return render(request, 'eventos/confirm_delete.html', {'evento': evento})
