import pandas as pd
import io
from ...etl.models import PacienteClinico
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from ...analytics.services.stats import MedicalStatsService

class ReportExporter:
    @staticmethod
    def get_dataframe():
        queryset = PacienteClinico.objects.all().values()
        if not queryset.exists():
            return pd.DataFrame()
        return pd.DataFrame(list(queryset))

    @classmethod
    def export_csv(cls):
        df = cls.get_dataframe()
        if df.empty:
            return ""
        return df.to_csv(index=False)

    @classmethod
    def export_excel(cls):
        df = cls.get_dataframe()
        buffer = io.BytesIO()
        if df.empty:
            df.to_excel(buffer, index=False)
        else:
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Pacientes')
        buffer.seek(0)
        return buffer.getvalue()

    @classmethod
    def export_pdf(cls):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Título
        elements.append(Paragraph("Reporte Ejecutivo de Pacientes Clínicos", styles['Title']))
        elements.append(Spacer(1, 12))

        # KPIs
        kpis = MedicalStatsService.get_kpis()
        elements.append(Paragraph("Indicadores Clave de Rendimiento (KPIs)", styles['Heading2']))
        
        kpi_data = [
            ["Métrica", "Valor"],
            ["Total Pacientes", str(kpis['total_pacientes'])],
            ["Pacientes Críticos", str(kpis['pacientes_criticos'])],
            ["Hipertensos", str(kpis['hipertensos'])],
            ["Diabéticos", str(kpis['diabeticos'])],
            ["Fumadores", str(kpis['fumadores'])],
            ["Riesgo Promedio (0-3)", str(kpis['riesgo_promedio'])]
        ]
        
        t_kpi = Table(kpi_data, colWidths=[200, 100])
        t_kpi.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t_kpi)
        elements.append(Spacer(1, 24))

        # Tabla Resumen (Últimos 10 críticos)
        elements.append(Paragraph("Últimos 10 Pacientes Críticos", styles['Heading2']))
        criticos = PacienteClinico.objects.filter(riesgo_enfermedad__iexact='Crítico').order_by('-id_paciente')[:10]
        
        if criticos.exists():
            table_data = [["ID", "Nombre", "Edad", "Sexo", "Diagnóstico"]]
            for p in criticos:
                table_data.append([
                    str(p.id_paciente),
                    f"{p.nombres} {p.apellidos}",
                    str(p.edad),
                    p.sexo,
                    p.diagnostico_preliminar
                ])
                
            t_criticos = Table(table_data, colWidths=[50, 150, 50, 80, 150])
            t_criticos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#dc3545")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(t_criticos)
        else:
            elements.append(Paragraph("No hay pacientes críticos registrados.", styles['Normal']))

        # Generar
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
