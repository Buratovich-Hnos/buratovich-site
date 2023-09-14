from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.list import MultipleObjectMixin
from django.template import loader


class DownloadCSVBaseClass(MultipleObjectMixin, View):
    filename = None
    fields = None
    headers = None
    template = None

    def get_csv_response(self):
        queryset = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        filename = self.filename
        if not filename.endswith('.csv'):
            filename += '.csv'
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        c = {
            'data': queryset,
            'headers': self.headers
        }
        t = loader.get_template(self.template)
        response.write(t.render(c))
        return response