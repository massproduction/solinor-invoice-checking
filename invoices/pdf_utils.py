import pdfkit

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from invoices.models import Invoice, HourEntry, WeeklyReport, WeeklyReportComments

from invoices.utils import latest_or_none, latest_change_of_scope_or_none

from statistics import mean


def generate_pdf(title, content, **custom_options):
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_CMD)
    wk_options = {
        'page-size': 'a4',
        'orientation': 'landscape',
        'title': title,
        # In order to specify command-line options that are simple toggles
        # using this dict format, we give the option the value None
        'no-outline': None,
        'disable-javascript': None,
        'encoding': 'UTF-8',
        'margin-left': '0.2cm',
        'margin-right': '0.2cm',
        'margin-top': '0.3cm',
        'margin-bottom': '0.3cm',
        'lowquality': None,
    }
    for option in custom_options:
        wk_options[option] = custom_options[option]

    return pdfkit.from_string(content,
                              False,
                              options=wk_options,
                              configuration=pdfkit_config)


def get_content_for_hour_report_pdf(entries, request):
    phases = {}
    for entry in entries:
        if entry.phase_name not in phases:
            phases[entry.phase_name] = []
        phases[entry.phase_name].append(entry)
    context = {
        "phases": phases,
        "STATIC_ROOT": settings.STATIC_ROOT
    }

    # We can generate the pdf from a url, file or, as shown here, a string
    return render_to_string('pdf_template.html', context=context, request=request)


def generate_hours_pdf_for_invoice(request, invoice):
    invoice_data = get_object_or_404(Invoice, invoice_id=invoice)
    title = replace_scandics(u"%s - %s - %s-%s" % (invoice_data.client, invoice_data.project, invoice_data.year, invoice_data.month))

    entries = HourEntry.objects.filter(project=invoice_data.project, client=invoice_data.client, date__year=invoice_data.year, date__month=invoice_data.month).filter(incurred_hours__gt=0)
    content = get_content_for_hour_report_pdf(entries, request)

    return generate_pdf(title, content), title


def generate_hours_pdf_for_weekly_report(request, weekly_report):
    weekly_report_data = get_object_or_404(WeeklyReport, weekly_report_id=weekly_report)
    title = replace_scandics(u"%s - %s - %s-%s" % (weekly_report_data.project_m.client, weekly_report_data.project_m.name, weekly_report_data.year, weekly_report_data.week))

    entries = HourEntry.objects.filter(project=weekly_report_data.project_m.name, client=weekly_report_data.project_m.client, date__year=weekly_report_data.year, date__week=weekly_report_data.week).filter(incurred_hours__gt=0)

    content = get_content_for_hour_report_pdf(entries, request)
    return generate_pdf(title, content), title


def replace_scandics(title):
    return title.replace(u"\xe4", u"a").replace(u"\xb6", u"o").replace(u"\x84", u"A").replace(u"\x96", u"O").replace(u"\xf6", "o")


def generate_weekly_report_pdf(request, weekly_report_id):
    weekly_report_data = get_object_or_404(WeeklyReport, weekly_report_id=weekly_report_id)
    title = replace_scandics("Weekly report for %s - %s - %s - %s" % (weekly_report_data.project_m.client, weekly_report_data.project_m.name, weekly_report_data.year, weekly_report_data.week))

    week_hour_entries = HourEntry.objects.filter(project=weekly_report_data.project_m.name, client=weekly_report_data.project_m.client, date__year=weekly_report_data.year, date__week=weekly_report_data.week).filter(incurred_hours__gt=0)
    persons = set(map((lambda x: x.user_m), week_hour_entries))

    week_hours_per_person = []
    for person in persons:
        week_hours_per_person.append({
            "name": person.display_name,
            "average_bill_rate": mean(list(map((lambda x: x.bill_rate), week_hour_entries.filter(user_id=person.user_id)))),
            "incurred_hours": sum(list(map((lambda x: x.incurred_hours), week_hour_entries.filter(user_id=person.user_id)))),
            "incurred_money": sum(list(map((lambda x: x.incurred_money), week_hour_entries.filter(user_id=person.user_id))))
        })

    print(week_hours_per_person)

    summary_this_week = latest_or_none(WeeklyReportComments, weekly_report_id=weekly_report_id, type="S")
    change_of_scope = latest_change_of_scope_or_none(weekly_report_data)
    custom_pages = WeeklyReportComments.objects.filter(weekly_report_id=weekly_report_id, type="CU")
    if custom_pages:
        custom_pages = list(map(lambda x: {"header": x.header, "bullets": x.text.splitlines()}, custom_pages))

    context = {
        "title": title,
        "STATIC_ROOT": settings.STATIC_ROOT,
        "week_hours_per_person": week_hours_per_person,
        "this_week_totals": {
            "total_hours": sum(map((lambda x: x.incurred_hours), week_hour_entries)),
            "total_money": sum(map((lambda x: x.incurred_money), week_hour_entries))
        },
        "summary_this_week_bullets": summary_this_week.text.splitlines() if hasattr(summary_this_week, "text") else None,
        "change_of_scope": {
            "bullets": change_of_scope.text.splitlines() if hasattr(change_of_scope, "text") else None,
            "last_changed": (str(change_of_scope.weekly_report.year) + " - " + str(change_of_scope.weekly_report.week)) if hasattr(change_of_scope, "weekly_report") else None
        },
        "custom_pages": custom_pages
    }

    content = render_to_string("weekly_report_pdf_template.html", context=context, request=request)
    extra_pdf_options = {"margin-bottom": "0", "margin-left": "0", "margin-right": "0", "margin-top": "0", "zoom": 1.5, "disable-smart-shrinking": None}

    return generate_pdf(title, content, **extra_pdf_options), title
