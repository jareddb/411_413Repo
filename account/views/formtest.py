from django_mako_plus import view_function
from django.http import HttpResponseRedirect
from django import forms
from formlib import Formless


@view_function
def process_request(request):

    # process the form
    form = TestForm(request)
    if form.is_valid():
        # do the work of the form
        # make the payment
        # create the user
        return HttpResponseRedirect('/homepage/contact')

    # render the template
    context = {
        'form': form,
    }
    return request.dmp_render('formtest.html', context)


class TestForm(Formless):
    def init(self):
        self.fields['comment'] = forms.CharField(label='Your comment')
        self.fields['renewal_date'] = forms.DateField(help_text="Enter a date between now and 4 weeks from now")


