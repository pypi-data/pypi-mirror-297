"""
Form definitions
"""

# Standard Library
import re

# Django
from django import forms
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# AA SRP
from aasrp.constants import KILLBOARD_DATA
from aasrp.managers import SrpManager
from aasrp.models import FleetType, Setting, SrpLink, SrpRequest, UserSetting

# Killboard URLs
zkillboard_base_url: str = KILLBOARD_DATA["zKillboard"]["base_url"]
evetools_base_url: str = KILLBOARD_DATA["EveTools"]["base_url"]
eve_kill_base_url: str = KILLBOARD_DATA["EVE-KILL"]["base_url"]

# Killboard regex
zkillboard_base_url_regex: str = KILLBOARD_DATA["zKillboard"]["base_url_regex"]
zkillboard_killmail_url_regex: str = KILLBOARD_DATA["zKillboard"]["killmail_url_regex"]
evetools_base_url_regex: str = KILLBOARD_DATA["EveTools"]["base_url_regex"]
evetools_killmail_url_regex: str = KILLBOARD_DATA["EveTools"]["killmail_url_regex"]
eve_kill_base_url_regex: str = KILLBOARD_DATA["EVE-KILL"]["base_url_regex"]
eve_kill_killmail_url_regex: str = KILLBOARD_DATA["EVE-KILL"]["killmail_url_regex"]


def get_mandatory_form_label_text(text: str) -> str:
    """
    Label text for mandatory form fields

    :param text:
    :type text:
    :return:
    :rtype:
    """

    required_text = _("This field is mandatory")
    required_marker = (
        f'<span aria-label="{required_text}" class="form-required-marker">*</span>'
    )

    return mark_safe(
        f'<span class="form-field-required">{text} {required_marker}</span>'
    )


class SrpLinkForm(ModelForm):
    """
    New SRP lnk form
    """

    srp_name = forms.CharField(
        required=True, label=get_mandatory_form_label_text(text=_("Fleet name"))
    )
    fleet_time = forms.DateTimeField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Fleet time")),
        widget=forms.DateTimeInput(attrs={"autocomplete": "off"}),
    )
    fleet_type = forms.ModelChoiceField(
        required=False,
        label=_("Fleet type (optional)"),
        queryset=FleetType.objects.filter(is_enabled=True),
        # empty_label=_("Please select a fleet type"),
    )
    fleet_doctrine = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Doctrine")),
    )
    aar_link = forms.CharField(required=False, label=_("After action report link"))

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = SrpLink
        fields = ["srp_name", "fleet_time", "fleet_type", "fleet_doctrine", "aar_link"]


class SrpLinkUpdateForm(ModelForm):
    """
    Edit SRP link update form
    """

    aar_link = forms.CharField(required=False, label=_("After action report link"))

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = SrpLink
        fields = ["aar_link"]


class SrpRequestForm(ModelForm):
    """
    SRP request form
    """

    killboard_link = forms.URLField(
        label=get_mandatory_form_label_text(text=_("Killboard link")),
        max_length=254,
        required=True,
        help_text=_(
            f"Find your kill mail on {zkillboard_base_url}, {evetools_base_url} or {eve_kill_base_url} and paste the link here."  # pylint: disable=line-too-long
        ),
    )

    additional_info = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 20, "input_type": "textarea"}),
        required=True,
        label=get_mandatory_form_label_text(text=_("Additional information")),
        help_text=_(
            "Please tell us about the circumstances of your untimely demise. "
            "Who was the FC, what doctrine was called, have changes to the fit "
            "been requested and so on. Be as detailed as you can."
        ),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = SrpRequest
        fields = ["killboard_link", "additional_info"]

    def clean_killboard_link(self):
        """
        Check if it's a link from one of the accepted kill boards and clean it

        :return:
        :rtype:
        """

        killboard_link = self.cleaned_data["killboard_link"]

        # Check if it's a link from one of the accepted kill boards
        if not any(
            re.match(pattern=regex, string=killboard_link)
            for regex in [
                zkillboard_base_url_regex,
                evetools_base_url_regex,
                eve_kill_base_url_regex,
            ]
        ):
            raise forms.ValidationError(
                message=_(
                    f"Invalid link. Please use {zkillboard_base_url}, {evetools_base_url} or {eve_kill_base_url}"  # pylint: disable=line-too-long
                )
            )

        # Check if it's an actual killmail
        if not any(
            re.match(pattern=regex, string=killboard_link)
            for regex in [
                zkillboard_killmail_url_regex,
                evetools_killmail_url_regex,
                eve_kill_killmail_url_regex,
            ]
        ):
            raise forms.ValidationError(
                message=_("Invalid link. Please post a link to a kill mail.")
            )

        # Check if there is already an SRP request for this kill mail
        killmail_id = SrpManager.get_kill_id(killboard_link=killboard_link)

        if SrpRequest.objects.filter(
            killboard_link__icontains="/kill/" + killmail_id
        ).exists():
            raise forms.ValidationError(
                message=_(
                    "There is already an SRP request for this kill mail. "
                    "Please check if you got the right one."
                )
            )

        return killboard_link


class SrpRequestPayoutForm(forms.Form):
    """
    Change payout value
    """

    value = forms.CharField(label=_("SRP payout value"), max_length=254, required=True)


class SrpRequestRejectForm(forms.Form):
    """
    SRP request reject form
    """

    reject_info = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 20, "input_type": "textarea"}),
        required=True,
        label=get_mandatory_form_label_text(text=_("Reject reason")),
        help_text=_("Please provide the reason this SRP request is rejected."),
    )


class SrpRequestAcceptForm(forms.Form):
    """
    SRP request accept form
    """

    reviser_comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 20, "input_type": "textarea"}),
        required=False,
        label=_("Comment (optional)"),
        help_text=_("Leave a comment for the requestor"),
    )


class SrpRequestAcceptRejectedForm(forms.Form):
    """
    SRP request accept rejected form
    """

    reviser_comment = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 10, "cols": 20, "input_type": "textarea"}),
        required=True,
        label=get_mandatory_form_label_text(text=_("Comment")),
        help_text=_(
            "Please provide the reason why this former rejected SRP request is now "
            "accepted."
        ),
    )


class UserSettingsForm(ModelForm):
    """
    User settings form
    """

    disable_notifications = forms.BooleanField(
        initial=False,
        required=False,
        label=_(
            "Disable notifications. "
            "(Auth and Discord, if a relevant module is installed)"
        ),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = UserSetting
        fields = ["disable_notifications"]


class SettingAdminForm(forms.ModelForm):
    """
    Form definitions for the FleetType form in admin
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta
        """

        model = Setting
        fields = "__all__"
        widgets = {"default_embed_color": forms.TextInput(attrs={"type": "color"})}
