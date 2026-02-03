import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import AbstractBaseUser
from django.template.defaultfilters import slugify
from rest_framework_api_key.models import AbstractAPIKey


class User(AbstractBaseUser):
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


class Product(models.Model):
    id = models.UUIDField(
        verbose_name=_("id"),
        help_text=_("primary key for the record as UUID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    nom_service_public_numerique = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(null=False, blank=False, unique=True)
    dataset_id = models.CharField(blank=True, null=False)

    class Meta:
        db_table = "product"
        verbose_name = _("product")
        verbose_name_plural = _("products")

    @property
    def last_indicators(self):
        recent_indicators = Indicator.objects.filter(productid=self).order_by("-date")
        if not recent_indicators:
            return []

        last_entry_date = recent_indicators[0].date
        return recent_indicators.filter(date=last_entry_date)

    @property
    def last_indicators_date(self):
        if len(self.last_indicators) != 0:
            return self.last_indicators[0].date

        return "N/A"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(self.nom_service_public_numerique)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_service_public_numerique


class Indicator(models.Model):
    id = models.UUIDField(
        verbose_name=_("id"),
        help_text=_("primary key for the record as UUID"),
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    productid = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        db_column="productId",
        related_name="indicators",
    )
    indicateur = models.CharField(max_length=100)
    valeur = models.FloatField()
    unite_mesure = models.CharField()
    frequence_monitoring = models.CharField()
    date = models.CharField()
    date_debut = models.CharField(blank=True, null=True)
    est_periode = models.BooleanField()
    est_automatise = models.BooleanField()
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
        db_table = "indicator"
        verbose_name = _("indicator")
        verbose_name_plural = _("indicators")
        unique_together = (("productid", "indicateur", "frequence_monitoring", "date"),)
        ordering = ("-date",)

    def save(self, *args, **kwargs):
        """Call `full_clean` before saving."""
        self.full_clean()
        return super().save(*args, **kwargs)


class ProductAPIKey(AbstractAPIKey):
    product = models.ForeignKey(
        "Product",
        models.DO_NOTHING,
        db_column="product",
        blank=False,
        null=False,
        related_name="api_keys",
    )

    class Meta:
        db_table = "api_keys"
        verbose_name = _("API key")
        verbose_name_plural = _("API keys")


class Adaptor(models.Model):
    product = models.ForeignKey(
        "Product",
        on_delete=models.PROTECT,
        db_column="product",
        related_name="adaptor",
    )
    indicator = models.CharField()

    source_url = models.CharField(blank=True, null=True)
    method = models.CharField(
        verbose_name=_("data fetching method"),
        help_text=_("name of the method used to fetch data"),
        blank=False,
        null=False,
    )

    status = models.CharField()
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        help_text=_("date and time at which a record was created"),
        auto_now_add=True,
        editable=False,
    )
    last_successful_run = models.DateTimeField(
        verbose_name=_("last successful run"), editable=False, blank=True, null=True
    )

    class Meta:
        db_table = "adaptor"
        verbose_name = _("Adaptor")
        verbose_name_plural = _("Adaptors")
        unique_together = (("product", "indicator"),)

    def get_last_month_data(self):
        """Call adaptor method to get last month's data."""
        adaptor = getattr(self.method, "get_last_month_data")
        return getattr(adaptor.method, "get_last_month_data")
