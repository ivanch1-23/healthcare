from apps.etl.models import PacienteClinico
from django.db.models import Q, Count

qs = PacienteClinico.objects.all()

print('1. TOTAL REGISTROS EN BD:', qs.count())

nulos = qs.filter(Q(glucosa__isnull=True) | Q(peso__isnull=True) | Q(temperatura__isnull=True))
print('2. REGISTROS CON NULOS (debe ser 0):', nulos.count())

print('3. VALORES DE SEXO (debe ser solo M y F):')
for item in qs.values('sexo').annotate(n=Count('sexo')).order_by('sexo'):
    print('  ', item)

print('4. DIAGNOSTICOS CON ERROR hipertencion (debe ser 0):', qs.filter(diagnostico_preliminar__icontains='hipertencion').count())
print('5. DIAGNOSTICOS CON ERROR hipertensíon con tilde mal (debe ser 0):', qs.filter(diagnostico_preliminar__exact='hipertensíon').count())

print('6. PESO OUTLIERS >300kg (debe ser 0):', qs.filter(peso__gt=300).count())
print('7. TEMPERATURA OUTLIERS <30 o >42 (debe ser 0):', qs.filter(Q(temperatura__lt=30) | Q(temperatura__gt=42)).count())

print('8. IDS DUPLICADOS (debe ser 0):')
dups = qs.values('id_paciente').annotate(n=Count('id_paciente')).filter(n__gt=1)
print('  ', dups.count())

print('9. EDADES NO NUMERICAS - min y max:')
from django.db.models import Min, Max
print('  ', qs.aggregate(min_edad=Min('edad'), max_edad=Max('edad')))

print('10. PRESION SISTOLICA - min y max:')
print('  ', qs.aggregate(Min('presion_sistolica'), Max('presion_sistolica')))
