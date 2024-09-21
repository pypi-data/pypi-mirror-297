"""
Forms
"""

# Django
from django import forms
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, URLValidator
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# CKEditor
from django_ckeditor_5.widgets import CKEditor5Widget

# AA Forum
from aa_forum.app_settings import discord_messaging_proxy_available
from aa_forum.helper.text import string_cleanup
from aa_forum.models import (
    Board,
    Category,
    General,
    Message,
    PersonalMessage,
    Setting,
    Topic,
    UserProfile,
)


def get_mandatory_form_label_text(text):
    """
    Returns a label text with a mandatory marker

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


class SpecialModelChoiceIterator(forms.models.ModelChoiceIterator):
    """
    Variant of Django's ModelChoiceIterator to prevent it from always re-fetching the
    given queryset from the database.
    """

    def __iter__(self):
        """
        Iterate over the choices

        :return:
        :rtype:
        """

        if self.field.empty_label is not None:
            yield "", self.field.empty_label

        queryset = self.queryset

        for obj in queryset:
            yield self.choice(obj=obj)


class SpecialModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    """
    Variant of Django's ModelMultipleChoiceField to prevent it from always
    re-fetching the given queryset from the database.
    """

    iterator = SpecialModelChoiceIterator

    def _get_queryset(self):
        """
        Get the queryset

        :return:
        :rtype:
        """

        return self._queryset

    def _set_queryset(self, queryset):
        """
        Set the queryset

        :param queryset:
        :type queryset:
        :return:
        :rtype:
        """

        self._queryset = queryset
        self.widget.choices = self.choices

    queryset = property(_get_queryset, _set_queryset)


class NewTopicForm(forms.Form):
    """
    New topic form
    """

    subject = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Subject")),
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": _("Subject")}),
    )

    message = forms.CharField(
        widget=CKEditor5Widget(
            config_name="extends",
            attrs={
                "class": "aa-forum-ckeditor django_ckeditor_5",
                "rows": 10,
                "cols": 20,
                "style": "width: 100%;",
            },
        ),
        required=False,  # We have to set this to False, otherwise CKEditor5 will not work
    )

    def clean(self):
        """
        Clean the form

        :return:
        :rtype:
        """

        cleaned_data = super().clean()

        if not string_cleanup(cleaned_data.get("message")).strip():
            raise ValidationError(_("You have forgotten the message!"))

        return cleaned_data

    def clean_message(self):
        """
        Cleanup the message

        :return:
        :rtype:
        """

        message = string_cleanup(string=self.cleaned_data["message"])

        return message


class EditTopicForm(ModelForm):
    """
    Edit category form
    """

    subject = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Subject")),
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": _("Subject")}),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = Topic
        fields = ["subject"]


class NewCategoryForm(ModelForm):
    """
    New category form
    """

    name = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Name")),
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": _("Category name")}),
    )
    boards = forms.CharField(
        required=False,
        label=_("Boards"),
        help_text=_(
            "Boards to be created with this category (One board per line). These "
            "boards will have no group restrictions, so you have to add them later "
            "where needed."
        ),
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "cols": 20,
                "input_type": "textarea",
                "placeholder": _("Boards"),
            }
        ),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = Category
        fields = ["name", "boards"]


class EditCategoryForm(ModelForm):
    """
    Edit category form
    """

    name = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Name")),
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": _("Category name")}),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = Category
        fields = ["name"]


class EditBoardForm(ModelForm):
    """
    Edit board form
    """

    name = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Name")),
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": _("Board name")}),
    )
    description = forms.CharField(
        required=False,
        label=_("Description"),
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "cols": 20,
                "input_type": "textarea",
                "placeholder": _("Board description (optional)"),
            }
        ),
    )
    groups = SpecialModelMultipleChoiceField(
        required=False,
        label=_("Group restrictions"),
        help_text=_(
            "This will restrict access to this board to the selected groups. If no "
            "groups are selected, everyone who can access the forum can also access "
            "this board. (This setting is optional)"
        ),
        queryset=Group.objects.all(),
    )
    discord_webhook = forms.CharField(
        required=False,
        label=_("Discord webhook (optional)"),
        help_text=_(
            "Discord webhook URL for the channel to post about new topics in this "
            "board. (This setting is optional)"
        ),
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "placeholder": "https://discord.com/api/webhooks/xxxxxxxxxxxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # pylint: disable=line-too-long
            }
        ),
    )
    use_webhook_for_replies = forms.BooleanField(
        initial=False,
        required=False,
        label=_("Use this Discord webhook for replies as well?"),
        help_text=_(
            "When activated every reply to any topic in this board will be "
            "posted to the defined Discord channel. (Child boards are excluded) "
            "Chose wisely! (Default: NO)"
        ),
    )
    is_announcement_board = forms.BooleanField(
        initial=False,
        required=False,
        label=_('Mark board as "Announcement Board"'),
        help_text=_(
            'Mark this board as an "Announcement Board", meaning that only certain '
            "selected groups can start new topics. All others who have access to this "
            "board will still be able to discuss in the topics though. This setting "
            "will not be inherited to child boards. (Default: NO)"
        ),
    )
    announcement_groups = SpecialModelMultipleChoiceField(
        required=False,
        label=_('Start topic restrictions for "Announcement Boards"'),
        help_text=_(
            "User in at least one of the selected groups will be able to start topics "
            'in "Announcement Boards". If no group is selected, only forum admins can '
            "do so. This setting will not be inherited to child boards. (Hint: These "
            "restrictions only take effect when a board is marked as "
            '"Announcement Board", see checkbox above.)'
        ),
        queryset=Group.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        """
        When form is initialized

        :param args:
        :param kwargs:
        """

        groups_queryset = kwargs.pop("groups_queryset", None)

        super().__init__(*args, **kwargs)

        if groups_queryset:
            self.fields["groups"].queryset = groups_queryset

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = Board
        fields = [
            "name",
            "description",
            "groups",
            "discord_webhook",
            "use_webhook_for_replies",
            "is_announcement_board",
            "announcement_groups",
        ]


class EditMessageForm(ModelForm):
    """
    Edit message form
    """

    close_topic = forms.BooleanField(
        required=False,
        label=_("Close topic"),
        help_text=_(
            "If checked, this topic will be closed after posting this message."
        ),
    )

    reopen_topic = forms.BooleanField(
        required=False,
        label=_("Reopen topic"),
        help_text=_(
            "If checked, this topic will be reopened after posting this message."
        ),
    )

    def __init__(self, *args, **kwargs):
        """
        When form is initialized

        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        """

        super().__init__(*args, **kwargs)

        # We have to set this to False, otherwise CKEditor5 will not work
        self.fields["message"].required = False

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = Message
        fields = ["message", "close_topic", "reopen_topic"]
        widgets = {
            "message": CKEditor5Widget(
                config_name="extends",
                attrs={
                    "class": "aa-forum-ckeditor django_ckeditor_5",
                    "rows": 10,
                    "cols": 20,
                    "style": "width: 100%;",
                },
            )
        }
        labels = {"message": get_mandatory_form_label_text(text=_("Message"))}

    def clean(self):
        """
        Clean the form

        :return:
        :rtype:
        """

        cleaned_data = super().clean()

        if not string_cleanup(cleaned_data.get("message")).strip():
            raise ValidationError(_("You have forgotten the message!"))

        return cleaned_data

    def clean_message(self):
        """
        Cleanup the message

        :return:
        :rtype:
        """

        message = string_cleanup(string=self.cleaned_data["message"])

        return message


class UserProfileForm(ModelForm):
    """
    Edit message form
    """

    website_title = forms.CharField(
        required=False,
        label=_("Website title"),
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": _("e.g.: My Homepage")}),
        help_text=_("Your website's title."),
    )
    website_url = forms.CharField(
        required=False,
        label=_("Website URL"),
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": "https://example.com"}),
        help_text=_(
            "Your website's URL. (Don't forget to also set a title for your website, "
            "otherwise this field will be ignored.)"
        ),
    )
    discord_dm_on_new_personal_message = forms.BooleanField(
        required=False,
        label=_("PM me on Discord when I get a new personal message"),
        help_text=(
            _(
                "Information: There is currently no module installed that can handle "
                "Discord direct messages. Have a chat with your IT guys to remedy this."
            )
            if discord_messaging_proxy_available() is False
            else ""
        ),
    )
    show_unread_topics_dashboard_widget = forms.BooleanField(
        required=False,
        label=_("Show unread topics as widget on the dashboard"),
        help_text=(
            _(
                "Activating this setting will ad a widget to your dashboard that shows unread topics in the forum."  # pylint: disable=line-too-long
            )
        ),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = UserProfile
        fields = [
            "signature",
            "website_title",
            "website_url",
            "discord_dm_on_new_personal_message",
            "show_unread_topics_dashboard_widget",
        ]
        widgets = {
            "signature": CKEditor5Widget(
                config_name="extends",
                attrs={
                    "class": "aa-forum-ckeditor django_ckeditor_5",
                    "rows": 10,
                    "cols": 20,
                    "style": "width: 100%;",
                },
            )
        }
        labels = {"signature": _("Signature")}
        help_texts = {"signature": _("Your signature will appear below your posts.")}

    def clean_signature(self):
        """
        Check that the signature is not longer than allowed

        :return:
        :rtype:
        """

        signature = string_cleanup(string=self.cleaned_data["signature"])

        if not signature:
            return ""

        max_signature_length = Setting.objects.get_setting(
            setting_key=Setting.Field.USERSIGNATURELENGTH
        )

        try:
            MaxLengthValidator(max_signature_length)(signature)
        except ValidationError as exc:
            raise ValidationError(
                _(
                    f"Ensure your signature has at most {max_signature_length} characters. (Currently: {len(signature)})"  # pylint: disable=line-too-long
                )
            ) from exc

        return signature

    def clean_website_url(self):
        """
        Check if it's a valid URL

        :return:
        :rtype:
        """

        website_url = self.cleaned_data["website_url"]

        if not website_url:
            return ""

        try:
            URLValidator()(website_url)
        except ValidationError as exc:
            raise ValidationError(_("This is not a valid URL")) from exc

        return website_url


class SettingForm(ModelForm):
    """
    Edit message form
    """

    messages_per_page = forms.IntegerField(
        required=True,
        label=get_mandatory_form_label_text(
            Setting.Field.MESSAGESPERPAGE.label  # pylint: disable=no-member
        ),
        help_text=_(
            "How many messages per page should be displayed in a forum topic? "
            "(Default: 15)"
        ),
    )
    topics_per_page = forms.IntegerField(
        required=True,
        label=get_mandatory_form_label_text(
            Setting.Field.TOPICSPERPAGE.label  # pylint: disable=no-member
        ),
        help_text=_(
            "How many topics per page should be displayed in a forum category? "
            "(Default: 10)"
        ),
    )
    user_signature_length = forms.IntegerField(
        required=True,
        label=get_mandatory_form_label_text(
            Setting.Field.USERSIGNATURELENGTH.label  # pylint: disable=no-member
        ),
        help_text=_(
            "How long (Number of characters) is a user's signature allowed to be? "
            "(Default: 750)"
        ),
    )

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = Setting
        fields = ["messages_per_page", "topics_per_page", "user_signature_length"]


class NewPersonalMessageForm(ModelForm):
    """
    New personal message form
    """

    recipient = forms.ModelChoiceField(
        queryset=User.objects.none(),
        required=True,
        label=get_mandatory_form_label_text(text=_("Recipient")),
    )
    subject = forms.CharField(
        required=True,
        label=get_mandatory_form_label_text(text=_("Subject")),
        max_length=254,
        widget=forms.TextInput(attrs={"placeholder": _("Hello there …")}),
    )

    def __init__(self, *args, **kwargs):
        """
        When form is initialized

        :param args:
        :param kwargs:
        """

        super().__init__(*args, **kwargs)

        self.fields["recipient"].queryset = General.users_with_basic_access()
        self.fields["message"].required = False

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = PersonalMessage
        fields = ["recipient", "subject", "message"]
        widgets = {
            "message": CKEditor5Widget(
                config_name="extends",
                attrs={
                    "class": "aa-forum-ckeditor django_ckeditor_5",
                    "rows": 10,
                    "cols": 20,
                    "style": "width: 100%;",
                },
            )
        }
        labels = {"message": get_mandatory_form_label_text(text=_("Message"))}

    def clean(self):
        """
        Clean the form

        :return:
        :rtype:
        """

        cleaned_data = super().clean()

        if not string_cleanup(cleaned_data.get("message")).strip():
            raise ValidationError(_("You have forgotten the message!"))

        return cleaned_data

    def clean_message(self):
        """
        Cleanup the message

        :return:
        :rtype:
        """

        message = string_cleanup(string=self.cleaned_data["message"])

        return message


class ReplyPersonalMessageForm(ModelForm):
    """
    Reply personal message form
    """

    def __init__(self, *args, **kwargs):
        """
        When form is initialized

        :param args:
        :param kwargs:
        """

        super().__init__(*args, **kwargs)

        self.fields["message"].required = False

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta definitions
        """

        model = PersonalMessage
        fields = ["message"]
        widgets = {
            "message": CKEditor5Widget(
                config_name="extends",
                attrs={
                    "class": "aa-forum-ckeditor django_ckeditor_5",
                    "rows": 10,
                    "cols": 20,
                    "style": "width: 100%;",
                },
            )
        }
        labels = {"message": get_mandatory_form_label_text(text=_("Message"))}

    def clean(self):
        """
        Clean the form

        :return:
        :rtype:
        """

        cleaned_data = super().clean()

        if not string_cleanup(cleaned_data.get("message")).strip():
            raise ValidationError(_("You have forgotten the message!"))

        return cleaned_data

    def clean_message(self):
        """
        Cleanup the message

        :return:
        :rtype:
        """

        message = string_cleanup(string=self.cleaned_data["message"])

        return message
