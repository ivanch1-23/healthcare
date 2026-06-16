from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from .services.exporter import ReportExporter
from drf_spectacular.utils import extend_schema, OpenApiParameter

class ExportReportView(APIView):
    """
    GET /api/reportes/exportar/
    Exporta la base de datos de pacientes clínicos en formato CSV, Excel o PDF.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(name='formato', description='Formato de exportación (csv, excel, pdf)', required=True, type=str)
        ]
    )
    def get(self, request):
        formato = request.query_params.get('formato', 'csv').lower()

        if formato == 'csv':
            csv_data = ReportExporter.export_csv()
            response = HttpResponse(csv_data, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="pacientes.csv"'
            return response
            
        elif formato == 'excel':
            excel_data = ReportExporter.export_excel()
            response = HttpResponse(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="pacientes.xlsx"'
            return response
            
        elif formato == 'pdf':
            pdf_data = ReportExporter.export_pdf()
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_ejecutivo.pdf"'
            return response
            
        else:
            return HttpResponse("Formato no soportado. Usa csv, excel o pdf.", status=400)
