import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser


class BaseModel(models.Model):
    """
    Serves as an abstract base model for other models, ensuring that records are validated
    before saving as Django doesn't do it by default.

    Includes fields common to all models: a UUID primary key and creation/update timestamps.
    """

    id = models.UUIDField(
        verbose_name=_("id"),
        help_text=_("primary key for the record as UUID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("date and time at which a record was created"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        help_text=_("date and time at which a record was last updated"),
        auto_now=True,
        editable=False,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Call `full_clean` before saving."""
        self.full_clean()
        return super().save(*args, **kwargs)


class User(AbstractBaseUser):
    email = models.EmailField(_("email address"))
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"


class Product(BaseModel):
    nom_service_public_numerique = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "product"
        verbose_name = _("product")
        verbose_name_plural = _("products")
        managed = False

    @property
    def last_indicators(self):
        recent_indicators = Indicator.objects.filter(product=self).order_by("date")
        last_entry_date = recent_indicators[0].date
        return recent_indicators.filter(date=last_entry_date)


class Indicator(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="indicators"
    )
    indicateur = models.CharField("utilisateurs actifs", max_length=100)
    valeur = models.FloatField()
    unite_mesure = models.CharField()
    frequence_monitoring = models.CharField()
    date = models.DateField()
    date_debut = models.DateField()
    est_periode = models.BooleanField()
    est_automatise = models.BooleanField()

    class Meta:
        db_table = "indicator"
        verbose_name = _("indicator")
        verbose_name_plural = _("indicators")
        managed = False
