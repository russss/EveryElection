import datetime

from django.http import HttpResponseRedirect
from django import forms
from formtools.wizard.views import NamedUrlSessionWizardView

from organisations.models import Organisation
from elections.models import Document, ElectedRole, ElectionSubType
from elections.utils import (
    create_ids_for_each_ballot_paper,
    get_notice_directory,
)
from elections.forms import (
    ElectionDateKnownForm,
    ElectionDateForm,
    ElectionTypeForm,
    ElectionSubTypeForm,
    ElectionOrganisationForm,
    ElectionOrganisationDivisionForm,
    ElectionSourceForm,
)
from election_snooper.models import SnoopedElection


FORMS = [
    ("source", ElectionSourceForm),
    ("date_known", ElectionDateKnownForm),
    ("date", ElectionDateForm),
    ("election_type", ElectionTypeForm),
    ("election_subtype", ElectionSubTypeForm),
    ("election_organisation", ElectionOrganisationForm),
    ("election_organisation_division", ElectionOrganisationDivisionForm),
    ("review", forms.Form),
]

TEMPLATES = {
    "source": "id_creator/source.html",
    "date_known": "id_creator/date_known.html",
    "date": "id_creator/date.html",
    "election_type": "id_creator/election_type.html",
    "election_subtype": "id_creator/election_subtype.html",
    "election_organisation": "id_creator/election_organisation.html",
    "election_organisation_division":
        "id_creator/election_organisation_division.html",
    "review": "id_creator/review.html",
}


def show_source_step(wizard):
    # if we've got a radar_id in the URL, we want to show the source form
    radar_id = wizard.request.GET.get('radar_id', False)
    if radar_id:
        return True

    # if a source is already set, we want to show the source form
    data = wizard.get_cleaned_data_for_step('source')
    if isinstance(data, dict) and 'source' in data:
        return True

    # otherwise, hide it
    return False


def show_date_known_step(wizard):
    # if we've already got a date in extra_data
    # we can skip the `date_known` form
    if isinstance(wizard.storage.extra_data, dict) and\
        wizard.storage.extra_data.get('radar_date', False):
        return False

    # if the user has submitted a 'Notice of Election' document
    # skip the `date_known` form (i.e: don't allow creating an id without
    # a date when we have a Notice of Election)
    data = wizard.get_cleaned_data_for_step('source')
    if isinstance(data, dict) and 'document' in data and data['document']:
        return False

    # otherwise, show it
    return True


def date_known(wizard):
    date_known_step_data = wizard.get_cleaned_data_for_step('date_known')
    if date_known_step_data:
        known = date_known_step_data.get('date_known')
        if known == "no":
            return False
    return True


def select_organisation(wizard):
    election_type = wizard.get_election_type()
    if not election_type:
        return False
    qs = ElectedRole.objects.filter(election_type=election_type)

    if qs.count() > 1:
        return True
    else:
        wizard.storage.extra_data.update({
            'election_organisation': [qs[0].organisation.slug, ]})

        return False


def select_subtype(wizard):
    election_type = wizard.get_election_type()
    if not election_type:
        return False
    subtypes = ElectionSubType.objects.filter(election_type=election_type)
    return subtypes.count() > 1


def select_organisation_division(wizard):
    election_type = wizard.get_election_type()
    if not election_type:
        return False
    if wizard.get_election_type().election_type == "mayor":
        return False
    return True



CONDITION_DICT = {
    'source': show_source_step,
    'date_known': show_date_known_step,
    'date': date_known,
    'election_organisation': select_organisation,
    'election_organisation_division': select_organisation_division,
    'election_subtype': select_subtype,
}


class IDCreatorWizard(NamedUrlSessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_election_type(self):
        if self.get_cleaned_data_for_step('election_type'):
            return self.get_cleaned_data_for_step(
                'election_type').get('election_type')

    def get_election_subtypes(self):
        if self.get_cleaned_data_for_step('election_subtype'):
            return self.get_cleaned_data_for_step(
                'election_subtype').get('election_subtype')

    def get_organisations(self):
        if self.get_cleaned_data_for_step('election_organisation'):
            return self.get_cleaned_data_for_step(
                'election_organisation').get('election_organisation')
        if 'election_organisation' in self.storage.extra_data:
            qs = Organisation.objects.filter(
                electedrole__election_type__election_type__in=\
                    self.storage.extra_data['election_organisation']
            )
            return qs

    def get_election_date(self):
        election_date = self.get_cleaned_data_for_step('date')
        if election_date:
            election_date = election_date['date']
        else:
            election_date = datetime.now()

        return election_date

    def get_form_initial(self, step):
        if step == 'source':

            # init the 'source' form with details of a SnoopedElection record
            radar_id = self.request.GET.get('radar_id', False)
            if radar_id:
                se = SnoopedElection.objects.get(pk=radar_id)
                if se.snooper_name == "CustomSearch:NoticeOfElectionPDF":
                    # put these in the session - they aren't user-modifiable
                    self.storage.extra_data.update({
                        'radar_id': se.id,
                        'radar_date': '',
                    })
                    # auto-populate the form with these to allow editing
                    return {
                        'source': se.detail_url,
                        'document': se.detail_url,
                    }
                elif se.snooper_name == "ALDC":
                    # put these in the session - they aren't user-modifiable
                    self.storage.extra_data.update({
                        'radar_id': se.id,
                        'radar_date': se.date,
                    })
                    # auto-populate the form with these to allow editing
                    return {
                        'source': se.source,
                        'document': '',
                    }
                else:
                    return {}

        if step == 'date':
            # if we've got a date from a SnoopedElection
            # init the date form with that
            if isinstance(self.storage.extra_data, dict) and\
                self.storage.extra_data.get('radar_date', False):

                radar_date = self.storage.extra_data['radar_date']
                if isinstance(radar_date, datetime.date):
                    return {
                        'date': [
                            radar_date.day,
                            radar_date.month,
                            radar_date.year
                        ]
                    }

        return self.initial_dict.get(step, {})

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        all_data = self.get_all_cleaned_data()
        # print("\n".join(str(all_data).split(',')))
        if not 'date' in all_data:
            all_data['date'] = None
        if not all_data.get('election_organisation'):
            all_data.update(self.storage.extra_data)
        context['all_data'] = all_data
        all_ids = create_ids_for_each_ballot_paper(all_data, self.get_election_subtypes())
        # all_ids = create_ids_grouped(all_data, self.get_election_subtypes())
        context['all_ids'] = all_ids
        return context

    def get_form_kwargs(self, step):
        if step in ["election_organisation", "election_subtype"]:
            election_type = self.get_election_type()
            if election_type:
                return {
                    'election_type': election_type.election_type
                }
        if step == "election_organisation_division":
            organisations = self.get_organisations()
            election_subtype = self.get_election_subtypes()

            return {
                'organisations': organisations,
                'election_subtype': election_subtype,
                'election_date': self.get_election_date(),
            }
        return {}

    def done(self, form_list, **kwargs):
        # Make the elections

        context = self.get_context_data(form_list)
        all_data = self.get_all_cleaned_data()

        # Attach Notice of Election doc
        if all_data.get('document', False):
            # only sync the Notice of Election doc to S3 once
            # (not once per ballot paper)
            directory = get_notice_directory(context['all_ids'])
            doc = Document()
            doc.source_url = all_data['document']
            doc.archive_document(all_data['document'], directory)
            doc.save()

            for election in context['all_ids']:
                # Attach Notice of Election docs to IDs we are creating
                # but only link the document to the individual ballot IDs
                # because we can't make a safe assumption about whether
                # all of the elections in a group are covered by a single
                # Notice of Election document - it will vary
                if not election.is_group_id:
                    election.notice = doc

        for election in context['all_ids']:
            election.save_model()

        return HttpResponseRedirect('/')
