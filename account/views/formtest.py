from django_mako_plus import view_function
from django import forms

@view_function
def process_request(request):

    #process the form
    form = TestForm()


    #render the form
    context = {
    }
    return request.dmp_render('formtest.html', context)

class TestForm(forms.Form):
    comment = forms.CharField(label='Your comment')
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks from now")


